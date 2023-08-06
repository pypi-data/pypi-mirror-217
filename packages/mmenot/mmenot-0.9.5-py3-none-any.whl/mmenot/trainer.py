import argparse
import logging
import os
import os.path as osp

from mmengine.config import Config
from mmengine.config import DictAction
from mmengine.logging import print_log
from mmengine.registry import RUNNERS
from mmengine.runner import Runner

from mmenot.utils.common import build_model_from_cfg
from mmenot.utils.common import from_cfg
from mmenot.utils.common import runner_save_checkpoint

Runner.from_cfg = classmethod(from_cfg)  # type: ignore
Runner.save_checkpoint = runner_save_checkpoint


def parse_args():  # pylint: disable=missing-function-docstring
    parser = argparse.ArgumentParser(description='Tune a model')
    parser.add_argument('config', help='train config file path')
    parser.add_argument('checkpoint', help='checkpoint file')
    parser.add_argument('--distill', action='store_true', default=False, help='enable distillation mode')
    parser.add_argument('--work-dir', help='the dir to save logs and models')
    parser.add_argument('--amp', action='store_true', default=False, help='enable automatic-mixed-precision training')
    parser.add_argument('--auto-scale-lr', action='store_true', help='enable automatically scaling LR.')
    parser.add_argument(
        '--resume',
        nargs='?',
        type=str,
        const='auto',
        help='If specify checkpoint path, resume from it, while if not '
        'specify, try to auto resume from the latest checkpoint '
        'in the work directory.',
    )
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.',
    )
    parser.add_argument('--launcher', choices=['none', 'pytorch', 'slurm', 'mpi'], default='none', help='job launcher')
    # When using PyTorch version >= 2.0.0, the `torch.distributed.launch`
    # will pass the `--local-rank` parameter to `tools/train.py` instead
    # of `--local_rank`.
    parser.add_argument('--local_rank', '--local-rank', type=int, default=0)
    args = parser.parse_args()
    if 'LOCAL_RANK' not in os.environ:
        os.environ['LOCAL_RANK'] = str(args.local_rank)

    return args


def train():  # pylint: disable=too-many-branches, missing-function-docstring
    args = parse_args()

    if args.distill:
        # pylint: disable=import-outside-toplevel
        from mmengine.registry import MODELS
        from mmrazor.utils import register_all_modules

        register_all_modules(init_default_scope=False)  # mmrazor
        MODELS.build_func = build_model_from_cfg

    try:
        # pylint: disable=import-outside-toplevel
        from mmdet.utils import setup_cache_size_limit_of_dynamo

        setup_cache_size_limit_of_dynamo()
    except ImportError:
        pass

    # load config
    cfg = Config.fromfile(args.config)
    cfg.launcher = args.launcher
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    # work_dir is determined in this priority: CLI > segment in file > filename
    if args.work_dir is not None:
        # update configs according to CLI args if args.work_dir is not None
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir', None) is None:
        # use config filename as default work_dir if cfg.work_dir is None
        cfg.work_dir = osp.join('./work_dirs', osp.splitext(osp.basename(args.config))[0])

    # enable automatic-mixed-precision training
    if args.amp:
        if getattr(cfg.optim_wrapper, 'type', None):
            optim_wrapper = cfg.optim_wrapper.type
            if optim_wrapper == 'AmpOptimWrapper':
                print_log(
                    msg='AMP training is already enabled in your config.',
                    logger='current',
                    level=logging.WARNING,
                )
            else:
                assert optim_wrapper == 'OptimWrapper', (
                    '`--amp` is only supported when the optimizer wrapper type is '
                    f'`OptimWrapper` but got {optim_wrapper}.'
                )
                cfg.optim_wrapper.type = 'AmpOptimWrapper'
                cfg.optim_wrapper.loss_scale = 'dynamic'

        # from mmrazor
        if getattr(cfg.optim_wrapper, 'constructor', None):
            if cfg.optim_wrapper.architecture.type == 'OptimWrapper':
                cfg.optim_wrapper.architecture.type = 'AmpOptimWrapper'
                cfg.optim_wrapper.architecture.loss_scale = 'dynamic'

    # enable automatically scaling LR
    if args.auto_scale_lr:
        if 'auto_scale_lr' in cfg and 'enable' in cfg.auto_scale_lr and 'base_batch_size' in cfg.auto_scale_lr:
            cfg.auto_scale_lr.enable = True
        else:
            raise RuntimeError(
                'Can not find "auto_scale_lr" or '
                '"auto_scale_lr.enable" or '
                '"auto_scale_lr.base_batch_size" in your'
                ' configuration file.'
            )

    # resume is determined in this priority: resume from > auto_resume
    if args.resume == 'auto':
        cfg.resume = True
        cfg.load_from = None
    elif args.resume is not None:
        cfg.resume = True
        cfg.load_from = args.resume

    # replace model config by checkpoint path
    if args.distill:
        cfg['model']['architecture'] = args.checkpoint
    else:
        cfg['model'] = args.checkpoint

    # build the runner from config
    if 'runner_type' not in cfg:
        # build the default runner
        runner = Runner.from_cfg(cfg)
    else:
        # build customized runner from the registry
        # if 'runner_type' is set in the cfg
        runner = RUNNERS.build(cfg)  # type: ignore

    # start training
    runner.train()


if __name__ == '__main__':
    train()
