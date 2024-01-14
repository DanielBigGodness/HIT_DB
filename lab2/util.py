import treePlotter


class util:
    __Employee = ["ENAME", "ESSN", "ADDRESS", "SALARY", "SUPERSSN", "DNO", "BDATE"]
    __Department = ["DNAME", "DNO", "MGRSSN", "MGRSTARTDATE"]
    __Works_on = ["ESSN", "PNO", "HOURS"]
    __Project = ["PNAME", "PNO", "PLOCATION", "DNO"]
    __table = {"EMPLOYEE": __Employee, "DEPARTMENT": __Department, "WORKS_ON": __Works_on, "PROJECT": __Project}
    __commend = ["SELECT", "PROJECTION"]
    __oneOp_commend = ["SELECT", "PROJECTION"]
    __twoOp_commend = ["JOIN"]

    '''
    :param sql: str,原始sql命令
    :return line: list,原始命令转化的列表
    '''
    def read_sql(self, sql):
        line = sql.replace("'", '').strip().split(" ")
        while '' in line:
            line.remove('')
        return line


    '''
    :param line: list,存储命令的列表
    :return tree: dict,由列表生成的字典树
    '''
    def creat_tree(self, line):
        tree = {}
        if (line[0] in self.__oneOp_commend):
            index_nextBracket = self.find_index_list(line, "]")
            str = ''
            for i in range(index_nextBracket[0] - 2):
                str = str + line[i + 2]
            child_tree = self.creat_tree(line[index_nextBracket[0] + 2:-1])
            tree[line[0] + " " + str] = {'': child_tree}
            return tree
        elif (line[0] == "("):
            index_join = self.find_index_list(line, "JOIN")
            index_dual_Bracket = self.find_dual_bracket(line, 0)
            if (len(index_join) == 0):
                return self.creat_tree(line[1:-1])
            if (index_dual_Bracket > index_join[0]):
                return self.creat_tree(line[1:-1])
            if (len(index_join) != 0):
                left_tree = self.creat_tree(line[:index_join[0]])
                right_tree = self.creat_tree(line[index_join[0] + 1:])
                tree["JOIN"] = {"left": left_tree, "right": right_tree}
                return tree
        else:
            return line[0]

    '''
    :param list: list,待查找的列表
    :param char: str,带查找的符号
    :return :list,特定列表中出现特定符号的下标
    '''
    def find_index_list(self, list, char):
        return [i for (i, j) in enumerate(list) if j == char]


    '''
    :param line: list,待处理的列表
    note 使用选择串接律优化
    '''
    def xuanze_chuanjie(self, line):
        line_temp = line
        index_and = self.find_index_list(line_temp, '&')
        if (len(index_and) != 0):
            i = index_and[0]
            line_temp.insert(i, "]")
            line_temp.insert(i + 1, "(")
            line_temp.append(")")
            line_temp.insert(i + 2, "SELECT")
            line_temp[i + 3] = "["
        return line_temp


    '''
    :param line: list, 待处理的列表
    note 选择与连接的分配率
    '''
    # 对一个列表line进行选择与连接的分配率的变换。它可以将一个选择操作分配到一个连接操作的两个子关系上，从而减少查询的数据量。
    # 这段代码的效果是将一个形如SELECT [a] FROM [b] JOIN [c]的查询语句变换为SELECT [a] FROM ([SELECT [a] FROM [b]] JOIN [c])的查询语句，从而只连接a属性的值。
    def xuanze_fenpei(self, line):
        line_temp = line
        index_select = self.find_index_list(line_temp, "SELECT")
        for i in range(len(index_select))[::-1]:
            index_join = self.find_index_list(line_temp, "JOIN")[0]
            right_bracket = self.find_dual_bracket(line_temp, index_select[i] + 1)
            attr = line_temp[index_select[i] + 2]
            round = self.find_childTree(line_temp, index_join)
            left_table = line_temp[self.find_table(line_temp, round["left_first"], round["left_last"])]
            right_table = line_temp[self.find_table(line_temp, round["right_first"], round["right_last"])]
            to_left = attr in self.__table[left_table]
            to_right = attr in self.__table[right_table]
            if (to_left):
                temp = line_temp[index_select[i]:right_bracket + 2]
                line_temp = line_temp[:index_select[i]] + line_temp[
                                                          right_bracket + 2:round["left_first"] + 1] + temp + line_temp[
                                                                                                              round[
                                                                                                                  "left_first"] + 1:
                                                                                                              round[
                                                                                                                  "left_last"] + 1] + [
                                ")"] + line_temp[round["left_last"] + 1:]
                line_temp.pop()
            elif (to_right):
                temp = line_temp[index_select[i]:right_bracket + 2]
                line_temp = line_temp[:index_select[i]] + line_temp[right_bracket + 2:round[
                                                                                          "right_first"] + 1] + temp + line_temp[
                                                                                                                       round[
                                                                                                                           "right_first"] + 1:]
        return line_temp


    '''
    :param line: list,待处理的列表
    return line_temp: list, 经过投影串接律处理后的列表
    '''
    # 对一个列表line进行投影串接律的变换。它可以将一个投影操作和一个串接操作的顺序交换，从而减少查询的数据量。
    # 效果是将一个形如[a,b,c] JOIN [d,e,f]的查询语句变换为[a] PROJECTION ([a,b,c] JOIN [d,e,f])的查询语句，从而只返回a属性的值
    def touying_chuanjie(self, line):
        line_temp = line
        index_comma = self.find_index_list(line_temp, ',')
        if (len(index_comma) != 0):
            i = index_comma[0]
            line_temp.insert(i, "]")
            line_temp.insert(i + 1, "(")
            line_temp.append(")")
            line_temp.insert(i + 2, "PROJECTION")
            line_temp[i + 3] = "["
        return line_temp

    '''
    :param line: list,待处理的列表
    return line_temp: list, 经过投影分配律处理后的列表
    '''
    # 将SELECT子句分配到JOIN子树的内部，从而减少查询的数据量
    def touying_fenpei(self, line):
        line_temp = line
        index_projection = self.find_index_list(line, "PROJECTION")
        if (len(index_projection) == 0):
            return line
        for i in range(len(index_projection))[::-1]:
            index_join = self.find_index_list(line_temp, "JOIN")[0]
            # attr = line_temp[index_projection[i]+2]
            attrs = self.find_projectattrs(line)
            round = self.find_childTree(line_temp, index_join)
            left_table = line_temp[self.find_table(line_temp, round["left_first"], round["left_last"])]
            right_table = line_temp[self.find_table(line_temp, round["right_first"], round["right_last"])]
            left_attrs = self.__table[left_table]
            right_attrs = self.__table[right_table]
            to_left = False
            to_right = False
            to_left_attrs = []
            to_right_attrs = []
            for j in range(len(attrs)):
                if (attrs[j] in left_attrs):
                    to_left = True
                    to_left_attrs += [attrs[j]] + [","]
                if (attrs[j] in right_attrs):
                    to_right = True
                    to_right_attrs += [attrs[j]] + [","]
            same_attrs = []
            for k in left_attrs:
                if (k in right_attrs):
                    same_attrs += [k, ","]
            same_attrs.pop()
            same_attrs.append("]")
            if (to_left and to_right):
                left_temp = ["PROJECTION", "["] + to_left_attrs + same_attrs
                right_temp = ["PROJECTION", "["] + to_right_attrs + same_attrs
            elif (to_left):
                left_temp = ["PROJECTION", "["] + to_left_attrs + same_attrs
                right_temp = ["PROJECTION"] + ["["] + same_attrs
            elif (to_right):
                right_temp = ["PROJECTION", "["] + to_right_attrs + same_attrs
                left_temp = ["PROJECTION"] + ["["] + same_attrs
            line_temp = line_temp[:round["left_first"] + 1] + left_temp + ["("] + line_temp[
                                                                                  round["left_first"] + 1:round[
                                                                                      "left_last"]] + [")"] \
                        + line_temp[round["left_last"]:round["right_first"] + 1] + right_temp + ["("] + line_temp[round[
                                                                                                                      "right_first"] + 1:] + [
                            ")"]
            return line_temp

    '''
    :param line: list,待处理的列表
    :param index: int, 所寻找子树的父节点所在的下标
    :return index_child_round: {"first":int,"last":int}或者{"left_first":int,"left_last":int,"right_first":int,"right_last":int}, 所寻找子树的范围（两个括号的下标）
    '''

    def find_childTree(self, line, index):
        if (line[index] in self.__oneOp_commend):
            first = self.find_dual_bracket(line, index + 1) + 1
            last = self.find_dual_bracket(line, first)
            return {"first": first, "last": last}
        elif (line[index] in self.__twoOp_commend):
            left_last = index - 1
            left_first = self.find_dual_bracket(line, left_last)
            right_first = index + 1
            right_last = self.find_dual_bracket(line, right_first)
            return {"left_first": left_first, "left_last": left_last, "right_first": right_first,
                    "right_last": right_last}
        elif (line[index] in list(self.__table.keys())):
            return {"first": index - 1, "last": index + 1}
        else:
            for i in range(len(line) - index):
                if (line[index + i] == "("):
                    first = index + i
                    last = self.find_dual_bracket(line, first)
                    return {"first": first, "last": last}

    '''
    :param line: list, 带查找的列表
    :return attrs :list, 投影的属性的列表
    '''

    def find_projectattrs(self, line):
        index_comma = self.find_index_list(line, ",")
        attrs = []
        if (len(index_comma) != 0):
            for i in range(len(index_comma)):
                attr1 = line[index_comma[i] - 1]
                attr2 = line[index_comma[i] + 1]
                if (attr1 not in attrs):
                    attrs.append(attr1)
                if (attr2 not in attrs):
                    attrs.append(attr2)
        else:
            index_projection = self.find_index_list(line, "PROJECTION")
            attrs.append(line[index_projection[0] + 2])
        return attrs

    '''
    :param line: list, 带查找的列表
    :return i: int, 与其对称的括号的下标
    '''

    def find_dual_bracket(self, line, index):
        sum = 0;
        if (line[index] != "(" and line[index] != "[" and line[index] != ")"):
            return -1
        if (line[index] == "("):
            for i in range(len(line) - index):
                if (line[index + i] == ")"):
                    sum = sum - 1
                    if (sum == 0):
                        return index + i
                if (line[index + i] == "("):
                    sum = sum + 1
        elif (line[index] == ")"):
            for i in range(index + 1)[::-1]:
                if (line[i] == "("):
                    sum = sum - 1
                    if (sum == 0):
                        return i
                if (line[i] == ")"):
                    sum = sum + 1
        else:
            for i in range(len(line) - index):
                if (line[index + i] == "]"):
                    sum = sum - 1
                    if (sum == 0):
                        return index + i
                if (line[index + i] == "["):
                    sum = sum + 1
        return -1

    '''
    :param line: list,待处理的列表
    :param first: int, 子树的前限下标
    :param last: int, 子树的后限下标
    :return : int, 子树中关系名的下标
    '''

    def find_table(self, line, first, last):
        for i in range(last - first):
            if (line[first + i] in list(self.__table.keys())):
                return first + i

    '''

    '''

    def merge(self, query):
        line = self.read_sql(query)
        mytree = self.creat_tree(line)
        treePlotter.createPlot(mytree)
        line = self.xuanze_chuanjie(line)
        line = self.xuanze_fenpei(line)
        line = self.touying_fenpei(line)
        mytree = self.creat_tree(line)
        treePlotter.createPlot(mytree)