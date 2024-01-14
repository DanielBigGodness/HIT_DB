import extmem
from config import project_dir, tuple_num
from extmem import Buffer, blk_num1, disk_dir

# 首先，使用extmem.drop_blk_in_dir(project_dir)函数删除project_dir文件夹下的所有模拟磁盘文件，以便存储投影的结果。
# 然后，初始化缓冲区buffer，用于读写磁盘块。同时，初始化一个空列表res，用于存储投影的结果，一个空集合all_res，用于去重，和一个计数器count，用于记录写入磁盘的块数。
# 接着，使用一个循环遍历关系R的所有磁盘块，每次从disk_dir文件夹中加载一个磁盘块到缓冲区中，使用buffer.load_blk('%sr%d.blk' % (disk_dir, disk_idx))函数返回该块在缓冲区中的索引index。
# 然后，使用一个嵌套循环遍历该块中的所有元组，每次从缓冲区中读取一个元组的数据，使用buffer.data[index]返回该元组的数据data。
# 接着，使用data.split()[0]函数提取该元组的A属性的值，如果该值不在all_res集合中，说明是一个新的值，那么就将该值添加到res列表和all_res集合中，使用res.append(data.split()[0])和all_res.add(data.split()[0])函数实现。
# 然后，判断res列表的长度是否等于tuple_num * 2，这是因为投影后只有一个属性A，所以一个磁盘块原来可以存储tuple_num个元组，现在可以存储tuple_num * 2个。如果是，那么就将res列表的内容写入到project_dir文件夹中的一个磁盘块中，使用buffer.write_buffer(res, '%sr%d.blk' % (project_dir, count))函数实现，并将res列表清空，count计数器加一，以便继续存储下一块的结果。
# 最后，当循环结束后，判断res列表是否为空，如果不为空，说明还有一些投影的结果没有写入到磁盘中，那么就将res列表的内容写入到project_dir文件夹中的最后一个磁盘块中，使用buffer.write_buffer(res, '%sr%d.blk' % (project_dir, count))函数实现。这样，就完成了对关系R的A属性的投影，并将投影的结果写入到磁盘中。
def relation_project(buffer: Buffer):
    """
    关系投影，对R的A属性进行投影并需要去重，并将结果写入到磁盘中
    :param buffer: 缓冲区
    """
    extmem.drop_blk_in_dir(project_dir)  # 删除文件夹下的所有模拟磁盘文件
    buffer.io_num, res, count, = 0, [], 0  # 投影选择的结果
    all_res = set()
    for disk_idx in range(blk_num1):
        index = buffer.load_blk('%sr%d.blk' % (disk_dir, disk_idx))  # 加载磁盘块内容到缓冲区中
        for data in buffer.data[index]:
            if data.split()[0] not in all_res:  # 去重
                res.append(data.split()[0])
                all_res.add(data.split()[0])
                # 因为投影后只有一个属性A，故一个blk原来可以存储tuple_num个元组，现在可以存储tuple_num*2个
                if len(res) == tuple_num * 2:
                    buffer.write_buffer(res, '%sr%d.blk' % (project_dir, count))
                    res, count = [], count + 1
        buffer.free_blk(index)
    if res:
        buffer.write_buffer(res, '%sr%d.blk' % (project_dir, count))