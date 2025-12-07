"""并发控制工具（优化版）

性能改进：
1. 动态并发限制（根据系统负载）
2. 分离不同验证类型的并发控制
3. 支持更高的并发数
4. 负载监控和自动调整
"""
import asyncio
import logging
from typing import Dict
import psutil

logger = logging.getLogger(__name__)

# 动态计算最大并发数
def _calculate_max_concurrency() -> int:
    """根据系统资源计算最大并发数"""
    try:
        cpu_count = psutil.cpu_count() or 4
        memory_gb = psutil.virtual_memory().total / (1024 ** 3)
        
        # 基于 CPU 和内存计算
        # 每个 CPU 核心支持 3-5 个并发任务
        # 每 GB 内存支持 2 个并发任务
        cpu_based = cpu_count * 4
        memory_based = int(memory_gb * 2)
        
        # 取两者的最小值，并设置上下限
        max_concurrent = min(cpu_based, memory_based)
        max_concurrent = max(10, min(max_concurrent, 100))  # 10-100 之间
        
        logger.info(
            f"系统资源: CPU={cpu_count}, Memory={memory_gb:.1f}GB, "
            f"计算并发数={max_concurrent}"
        )
        
        return max_concurrent
        
    except Exception as e:
        logger.warning(f"无法获取系统资源信息: {e}, 使用默认值")
        return 20  # 默认值

# 计算每种验证类型的并发限制
_base_concurrency = _calculate_max_concurrency()

# 为不同类型的验证创建独立的信号量
# 这样可以避免一个类型的验证阻塞其他类型
_verification_semaphores: Dict[str, asyncio.Semaphore] = {
    "gemini_one_pro": asyncio.Semaphore(_base_concurrency // 3),
    "chatgpt_teacher_k12": asyncio.Semaphore(_base_concurrency // 3),
    "bolt_teacher": asyncio.Semaphore(_base_concurrency // 3),
}


def get_verification_semaphore(verification_type: str) -> asyncio.Semaphore:
    """获取指定验证类型的信号量
    
    Args:
        verification_type: 验证类型
        
    Returns:
        asyncio.Semaphore: 对应的信号量
    """
    semaphore = _verification_semaphores.get(verification_type)
    
    if semaphore is None:
        # 未知类型，创建默认信号量
        semaphore = asyncio.Semaphore(_base_concurrency // 3)
        _verification_semaphores[verification_type] = semaphore
        logger.info(
            f"为新验证类型 {verification_type} 创建信号量: "
            f"limit={_base_concurrency // 3}"
        )
    
    return semaphore


def get_concurrency_stats() -> Dict[str, Dict[str, int]]:
    """获取并发统计信息
    
    Returns:
        dict: 各验证类型的并发信息
    """
    stats = {}
    for vtype, semaphore in _verification_semaphores.items():
        # 注意：_value 是内部属性，可能在不同 Python 版本中变化
        try:
            available = semaphore._value if hasattr(semaphore, '_value') else 0
            limit = _base_concurrency // 3
            in_use = limit - available
        except Exception:
            available = 0
            limit = _base_concurrency // 3
            in_use = 0
        
        stats[vtype] = {
            'limit': limit,
            'in_use': in_use,
            'available': available,
        }
    
    return stats


async def monitor_system_load() -> Dict[str, float]:
    """监控系统负载
    
    Returns:
        dict: 系统负载信息
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'concurrency_limit': _base_concurrency,
        }
    except Exception as e:
        logger.error(f"监控系统负载失败: {e}")
        return {
            'cpu_percent': 0.0,
            'memory_percent': 0.0,
            'concurrency_limit': _base_concurrency,
        }


def adjust_concurrency_limits(multiplier: float = 1.0):
    """动态调整并发限制
    
    Args:
        multiplier: 调整倍数（0.5-2.0）
    """
    global _verification_semaphores, _base_concurrency
    
    # 限制倍数范围
    multiplier = max(0.5, min(multiplier, 2.0))
    
    new_base = int(_base_concurrency * multiplier)
    new_limit = max(5, min(new_base // 3, 50))  # 每种类型 5-50
    
    logger.info(
        f"调整并发限制: multiplier={multiplier}, "
        f"new_base={new_base}, per_type={new_limit}"
    )
    
    # 创建新的信号量
    for vtype in _verification_semaphores.keys():
        _verification_semaphores[vtype] = asyncio.Semaphore(new_limit)


# 负载监控任务
_monitor_task = None

async def start_load_monitoring(interval: float = 60.0):
    """启动负载监控任务
    
    Args:
        interval: 监控间隔（秒）
    """
    global _monitor_task
    
    if _monitor_task is not None:
        return
    
    async def monitor_loop():
        while True:
            try:
                await asyncio.sleep(interval)
                
                load_info = await monitor_system_load()
                cpu = load_info['cpu_percent']
                memory = load_info['memory_percent']
                
                logger.info(
                    f"系统负载: CPU={cpu:.1f}%, Memory={memory:.1f}%"
                )
                
                # 自动调整并发限制
                if cpu > 80 or memory > 85:
                    # 负载过高，降低并发
                    adjust_concurrency_limits(0.7)
                    logger.warning("系统负载过高，降低并发限制")
                elif cpu < 40 and memory < 60:
                    # 负载较低，可以提高并发
                    adjust_concurrency_limits(1.2)
                    logger.info("系统负载较低，提高并发限制")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"负载监控异常: {e}")
    
    _monitor_task = asyncio.create_task(monitor_loop())
    logger.info(f"负载监控已启动: interval={interval}s")


async def stop_load_monitoring():
    """停止负载监控任务"""
    global _monitor_task
    
    if _monitor_task is not None:
        _monitor_task.cancel()
        try:
            await _monitor_task
        except asyncio.CancelledError:
            pass
        _monitor_task = None
        logger.info("负载监控已停止")
