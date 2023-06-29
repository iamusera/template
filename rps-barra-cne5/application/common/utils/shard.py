

def get_curr_shard(table_list: list, curr: int, total: int):
    """
    序列分片
    :param table_list 需要切分的序列
    :param curr: 当前分片序号，从1开始
    :param total: 分片总数
    :returns 当前分片序列
    """
    # 子任务数量
    count = len(table_list)
    # 计算商，每页个数
    size = int(count / total)
    task_idx_base = (curr - 1) * size
    # 计算当前片的子任务序列
    task_list = []
    # 分页逻辑计算
    for i in range(0, size):
        task_idx = task_idx_base + i
        if task_idx < count:
            task_list.append(table_list[task_idx])
    # 计算余数
    remainder = count % total
    # 余下的
    remainder_idx = count - remainder
    for i in range(0, remainder):
        if i + 1 == curr:
            remainder_idx += i
            if remainder_idx < count:
                task_list.append(table_list[remainder_idx])

    return task_list

