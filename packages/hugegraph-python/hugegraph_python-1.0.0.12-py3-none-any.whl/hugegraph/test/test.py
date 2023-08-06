from hugegraph.connection import PyHugeGraph

if __name__ == '__main__':
    client = PyHugeGraph("127.0.0.1", "8080", user="admin", pwd="admin", graph="hugegraph")

    """system"""
    res = client.get_graphinfo()
    print(res)
    res = client.get_all_graphs()
    print(res)
    res = client.get_version()
    print(res)
    res = client.get_graph_config()
    print(res)

    """schema"""
    schema = client.schema()
    schema.propertyKey("name").asText().ifNotExist().create()
    schema.propertyKey("birthDate").asText().ifNotExist().create()
    schema.vertexLabel("Person").properties("name", "birthDate").usePrimaryKeyId().primaryKeys(
        "name").ifNotExist().create()
    schema.vertexLabel("Movie").properties("name").usePrimaryKeyId().primaryKeys("name").ifNotExist().create()
    schema.edgeLabel("ActedIn").sourceLabel("Person").targetLabel("Movie").ifNotExist().create()

    print(schema.getVertexLabels())
    print(schema.getEdgeLabels())
    print(schema.getRelations())

    """graph"""
    g = client.graph()
    g.addVertex("Person", {"name": "Al Pacino", "birthDate": "1940-04-25"})
    g.addVertex("Person", {"name": "Robert De Niro", "birthDate": "1943-08-17"})
    g.addVertex("Movie", {"name": "The Godfather"})
    g.addVertex("Movie", {"name": "The Godfather Part II"})
    g.addVertex("Movie", {"name": "The Godfather Coda The Death of Michael Corleone"})

    g.addEdge("ActedIn", "12:Al Pacino", "13:The Godfather", {})
    g.addEdge("ActedIn", "12:Al Pacino", "13:The Godfather Part II", {})
    g.addEdge("ActedIn", "12:Al Pacino", "13:The Godfather Coda The Death of Michael Corleone", {})
    g.addEdge("ActedIn", "12:Robert De Niro", "13:The Godfather Part II", {})

    res = g.getVertexById("12:Al Pacino").label
    # g.removeVertexById("12:Al Pacino")
    print(res)
    g.close()

    """gremlin"""
    g = client.gremlin()
    res = g.exec("g.V().limit(10)")
    print(res)
