"""FZM and QXH lab1"""
# standard import
import re  # 导入正则表达式库用于文本处理
import random  # 导入random库用于生成随机数
import json
import heapq
# third party import
import networkx as nx  # 仅用于绘图函数
import matplotlib.pyplot as plt  # 仅用于绘图函数

GRAPH_FILENAME = 'C:/fzm2024/fzmLab1/Lab1_2021112472/data/graph.json'


def preprocess_text(text):
    """预处理文本"""
    # 使用正则表达式替换非字母字符为空格
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # 合并多余的空格
    # 正则表达式 `\s+` 匹配一个或多个连续的空白字符（包括空格、制表符、换行符等）。
    text = re.sub(r'\s+', ' ', text)

    # 转换文本为小写 `lower()` 函数将文本中的所有大写字母转换为小写字母。
    return text.lower().strip()


def create_directed_graph(text):
    """构建图"""
    # 使用空格将文本分割成单词列表
    words = text.split()

    # 初始化一个空字典来构建图，键是单词，值是另一个字典，表示与相邻出现在该单词之后的单词及其出现次数
    graph = {}

    # 遍历单词列表，除了最后一个单词（因为没有下一个单词与之形成边）
    for i in range(len(words) - 1):
        # 如果当前单词已经在图中
        if words[i] in graph:
            # 如果下一个单词已经与当前单词形成边，增加这条边的权重（出现次数）
            if words[i + 1] in graph[words[i]]:
                graph[words[i]][words[i + 1]] += 1
            else:
                # 如果当前单词与下一个单词还没有形成边，创建这条边并设置初始权重为1
                graph[words[i]][words[i + 1]] = 1
        else:
            # 如果当前单词不在图中，添加当前单词到图中，并创建一条到下一个单词的边，权重为1
            graph[words[i]] = {words[i + 1]: 1}

    # 处理最后一个单词，确保它也在图中，如果没有下一个单词与它相连，则其值为空字典
    if words[-1] not in graph:
        graph[words[-1]] = {}  # 确保最后一个词在图中

    # 返回构建的图
    return graph


def save_graph_json(graph, file_path):
    """保存图"""
    # 将图的字典格式转换为可以序列化的格式（即转换所有内部字典为字符串）
    json_graph = \
        {node: dict(neighbours.items()) for node, neighbours in graph.items()}
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(json_graph, file, indent=4)


def load_graph_json(file_path):
    """加载图"""
    with open(file_path, 'r', encoding="utf-8") as file:
        json_graph = json.load(file)
    # 将读取的 JSON 对象转换回原始的字典格式
    graph = \
        {node: dict(neighbours.items()) for node, neighbours in json_graph.items()}
    return graph


def show_directed_graph():
    """show graph"""
    graph = load_graph_json(GRAPH_FILENAME)
    # 使用 NetworkX 的 DiGraph() 函数创建一个有向图对象。
    # DiGraph 表示有向图，这种图中的边有方向，从一个节点指向另一个节点。
    nx_graph = nx.DiGraph()

    # 遍历输入的图的每个节点及其边缘，输入的图是一个字典格式，键是起始节点，值是另一个字典，表示目标节点和权重。
    for start, edges in graph.items():
        # 再次遍历字典，这次是遍历边和它们的权重
        for end, weight in edges.items():
            # 在网络图中添加一条边，起点是 start，终点是 end，权重是 weight
            nx_graph.add_edge(start, end, weight=weight)

    # 使用 Kamada-Kawai 布局算法是一种力导向布局算法，用于在图中定位节点。
    # 它尝试在二维空间中放置节点，以使得图的边尽可能地不重叠，并保持较短的边的长度，以便更清晰地展示图的结构。
    pos = nx.kamada_kawai_layout(nx_graph)

    # 获取网络图中所有边的权重属性，返回一个字典，键是边的元组（起点，终点），值是权重。
    weights = \
        nx.get_edge_attributes(nx_graph, 'weight')

    # 使用 draw 函数绘制网络图。参数 pos 定义了节点的位置，
    # with_labels=True 显示节点的标签，node_color 设置节点的颜色。
    nx.draw(nx_graph, pos, with_labels=True,
            node_color='skyblue', node_size=1000,
            edge_color='gray', arrowsize=10,
            font_size=10, font_weight='bold')
    # 使用 draw_networkx_edge_labels 函数在网络图中的边上显示标签（在这里是权重）。
    nx.draw_networkx_edge_labels(nx_graph, pos,
                                 edge_labels=weights,
                                 font_color='red', font_size=8)
    # 显示图形。这会打开一个窗口显示绘制的网络图，是 matplotlib.pyplot 的功能。
    plt.show()


def query_bridge_words(word1, word2):
    """查询桥接词"""
    graph = load_graph_json(GRAPH_FILENAME)
    if word1 == "" or word2 == "":
        return "Word1 and word2 cannot be empty!"

    if not word1.isalpha() or not word2.isalpha():
        return "Word1 and word2 should only contain English letters!"

    # 检查输入的两个单词是否都在图中。如果任意一个单词不在图中，则返回包含这些单词名称的错误信息。
    if word1 not in graph or word2 not in graph:
        missing_words = []
        if word1 not in graph:
            missing_words.append(word1)
        if word2 not in graph:
            missing_words.append(word2)
        return "No " + \
            ", ".join(['\"' + word + '\"' for word in missing_words]) \
            + " in the graph!"

    # 寻找桥接词。桥接词是指从 word1 可以直接到达的单词，并且这些单词可以直接到达 word2。
    bridge_words = \
        [node for node in graph[word1] if
         node in graph and word2 in graph[node]]

    # 如果没有找到任何桥接词，返回包含 word1 和 word2 的错误信息。
    if not bridge_words:
        return f"No bridge words from \"{word1}\" to \"{word2}\"!"

    # 如果找到桥接词，将它们组合成字符串并返回。
    return f"The bridge words from \"{word1}\" to \"{word2}\" are: " + \
        ", ".join(bridge_words) + "."


def generate_new_text(input_text):
    """生成新文本"""
    graph = load_graph_json(GRAPH_FILENAME)

    words = preprocess_text(input_text)
    # 将输入文本按空格分割成单词列表。
    words = words.split()

    # 初始化新文本，首先添加输入文本的第一个单词。
    new_text = words[0]

    # 遍历输入单词列表，从第二个单词开始（索引为1），因为第一个单词已经被添加到新文本中。
    for i in range(1, len(words)):
        # 寻找桥接词。
        # 通过检查图中是否存在从上一个单词 (words[i-1]) 到当前单词 (words[i]) 的桥接词。
        if words[i - 1] in graph and words[i] in graph:
            bridge_words = [node for node in graph[words[i - 1]] if
                            node in graph and words[i] in graph[node]]
            # 如果存在桥接词列表，从中随机选择一个桥接词并添加到新文本中。
            if bridge_words:
                new_text += ' ' + random.choice(bridge_words)

        # 然后将当前遍历到的单词 (words[i]) 添加到新文本中。
        new_text += ' ' + words[i]

    # 最终返回生成的新文本。
    return new_text


def calc_shortest_path(word1, word2):
    """最短路径计算"""
    graph = load_graph_json(GRAPH_FILENAME)
    # 检查起点和终点是否在图中
    if word1 not in graph or word2 not in graph:
        missing_words = [word for word in [word1, word2] if word not in graph]
        return "No " + ", ".join(['\"' + word + '\"' for word in missing_words]) + " in the graph!"
    # 使用优先队列（堆）来实现 Dijkstra 算法
    # 队列中存储的元素是一个元组，(累积的路径长度, 当前的单词, 路径)
    priority_queue = []
    heapq.heappush(priority_queue, (0, word1, [word1]))
    # 用于记录到每个节点的最短路径长度
    distances = {word1: 0}
    # 当队列不为空时，循环执行
    while priority_queue:
        # 弹出累积权重最小的元素
        current_distance, current, path = heapq.heappop(priority_queue)
        # 如果当前节点是目标单词，返回路径及路径权重
        if current == word2:
            return f"Shortest path: {' -> '.join(path)}\n" f"Path weight: {current_distance}"
        # 遍历当前节点的所有邻居
        for neighbor, weight in graph[current].items():
            distance = current_distance + weight
            # 如果当前路径到邻居的距离更短，或邻居尚未被访问
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue,(distance, neighbor, path + [neighbor]))
    # 如果找不到从起点到终点的路径
    return f"No path from \"{word1}\" to \"{word2}\""


def random_walk():
    """随机游走"""
    # 从 JSON 文件中加载图，其中 GRAPH_FILENAME 是一个全局变量，存储图数据文件的名称。
    graph = load_graph_json(GRAPH_FILENAME)

    # 使用 random.choice 随机选择图中的一个起始节点。
    start = random.choice(list(graph.keys()))

    # 初始化路径列表，起始只包含选择的起始节点。
    path = [start]

    # 初始化一个集合，用于记录访问过的边，防止走回头路。
    visited = set()

    # 无限循环执行随机游走，直到遇到终止条件。
    while True:
        # 获取当前路径的最后一个节点，即当前位置。
        current = path[-1]

        # 如果当前节点没有邻接节点（即边字典为空），则终止循环。
        if not graph[current]:
            break

        # 从当前节点的邻接节点中随机选择一个作为下一个节点。
        next_node = random.choice(list(graph[current].keys()))

        # 检查是否已经访问过当前节点到下一个节点的边，如果是，则终止循环，避免形成环。
        if (current, next_node) in visited:
            path.append(next_node)  # 将节点加入路径，表明走到这里终止。
            break

        # 将选择的下一个节点添加到路径中。
        path.append(next_node)

        # 将当前节点到下一个节点的边添加到已访问集合中。
        visited.add((current, next_node))

    # 将路径中的节点列表转换为用空格分隔的字符串返回。
    return ' '.join(path)


def main():
    """main"""
    # file_path = input("Enter the path to the text file: ")  # 输入文件路径
    file_path = 'C:/fzm2024/fzmLab1/Lab1_2021112472/data/test1.txt'

    with open(file_path, 'r', encoding="utf-8") as file:
        text = file.read()  # 读取文件内容

    processed_text = preprocess_text(text)  # 预处理文本
    graph = create_directed_graph(processed_text)  # 创建有向图
    save_graph_json(graph, GRAPH_FILENAME)  # 使用 JSON保存图

    while True:
        # 提供菜单选项
        print("\nFZM and QXH")
        print("1. Show Directed Graph")
        print("2. Query Bridge Words")
        print("3. Generate New Text")
        print("4. Calculate Shortest Path")
        print("5. Random Walk")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            show_directed_graph()
        elif choice == '2':
            word1 = input("Enter the first word: ")
            word2 = input("Enter the second word: ")
            print(query_bridge_words(word1, word2))
        elif choice == '3':
            input_text = input("Enter a line of text: ")
            print("Generated text:", generate_new_text(input_text))
        elif choice == '4':
            word1 = input("Enter the first word: ")
            word2 = input("Enter the second word: ")
            print(calc_shortest_path(word1, word2))
        elif choice == '5':
            print("Random walk output:", random_walk())
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please choose again.")


if __name__ == '__main__':
    main()
