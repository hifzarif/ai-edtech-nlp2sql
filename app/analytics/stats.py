queries = []

def log_query(question, time_taken):
    queries.append({"q": question, "time": time_taken})

def get_stats():
    total = len(queries)
    slowest = max(queries, key=lambda x: x["time"], default=None)

    keywords = {}
    for q in queries:
        for word in q["q"].split():
            keywords[word] = keywords.get(word, 0) + 1

    return {
        "total_queries": total,
        "common_keywords": sorted(keywords.items(), key=lambda x: -x[1])[:5],
        "slowest_query": slowest
    }