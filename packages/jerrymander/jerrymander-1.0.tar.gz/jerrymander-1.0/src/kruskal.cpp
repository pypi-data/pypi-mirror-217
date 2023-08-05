#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <vector>
#include <utility>
#include <queue>
#include <map>
#include <algorithm>
#include <random>
#include <cstdlib>
#include <ctime>

namespace py = pybind11;

struct Node
{
  std::pair<int, int> node;

  Node() : node(0, 0) {}
  Node(int val1, int val2) : node(val1, val2) {}

  int operator[](int index) const
  {
    return index == 0 ? node.first : node.second;
  }

  bool operator<(const Node &other) const
  {
    return node.first != other[0] ? node.first < other[0] : node.second < other[1];
  }

  bool operator==(const Node &other) const
  {
    return node.first == other[0] && node.second == other[1];
  }
};

struct Edge
{
  std::pair<Node, Node> edge;

  Edge() : edge(Node(), Node()) {}
  Edge(Node n1, Node n2) : edge(n1, n2) {}

  Node operator[](int index) const
  {
    return index == 0 ? edge.first : edge.second;
  }
};


class UnionFind
{
private:
  std::vector<int> parent;
  std::vector<int> rank;

public:
  UnionFind(int n)
  {
    parent = std::vector<int>(n);
    rank = std::vector<int>(n, 0);
    for (int i = 0; i < n; ++i)
      parent[i] = i;
  }

  int find(int x)
  {
    if (parent[x] != x)
      parent[x] = find(parent[x]); // Path compression
    return parent[x];
  }

  void unionSets(int x, int y)
  {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY)
    {
      if (rank[rootX] > rank[rootY])
      {
        parent[rootY] = rootX;
      }
      else if (rank[rootX] < rank[rootY])
      {
        parent[rootX] = rootY;
      }
      else
      {
        parent[rootY] = rootX;
        rank[rootX]++;
      }
    }
  }

  bool connected(int x, int y)
  {
    return find(x) == find(y);
  }
};

// Custom type caster specialization for Node
namespace pybind11
{
  namespace detail
  {
    template <>
    struct type_caster<Node>
    {
    public:
      PYBIND11_TYPE_CASTER(Node, _("Node"));

      // Python -> C++
      bool load(handle src, bool convert)
      {
        if (!isinstance<py::tuple>(src) || py::cast<py::tuple>(src).size() != 2)
          return false;
        py::tuple srcTuple = py::cast<py::tuple>(src);
        value = Node(py::cast<int>(srcTuple[0]), py::cast<int>(srcTuple[1]));
        return true;
      }

      // C++ -> Python
      static handle cast(const Node &src, return_value_policy /* policy */, handle /* parent */)
      {
        return py::make_tuple(src[0], src[1]).release();
      }
    };
  }
}

namespace pybind11
{
  namespace detail
  {
    template <>
    struct type_caster<Edge>
    {
    public:
      PYBIND11_TYPE_CASTER(Edge, _("Edge"));

      // Python -> C++
      bool load(handle src, bool convert)
      {
        if (!isinstance<py::tuple>(src) || py::cast<py::tuple>(src).size() != 2)
          return false;
        py::tuple srcTuple = py::cast<py::tuple>(src);
        value = Edge(py::cast<Node>(srcTuple[0]), py::cast<Node>(srcTuple[1]));
        return true;
      }

      // C++ -> Python
      static handle cast(const Edge &src, return_value_policy /* policy  */, handle /* parent */)
      {
        return py::make_tuple(src[0], src[1]).release();
      }
    };
  }
}

PYBIND11_MODULE(jerry, m)
{
  m.doc() = "pybind11 example plugin"; // optional module docstring

  m.def("rand_kruskal", [](const std::vector<Edge> &edges, const int num_nodes) -> std::vector<Edge>
        {
          std::vector<Edge> mst;

          // Create a mapping from Node to integer.
          std::map<Node, int> node_to_int;
          int node_count = 0;
          for (const auto &e : edges)
          {
            if (node_to_int.find(e[0]) == node_to_int.end())
              node_to_int[e[0]] = node_count++;
            if (node_to_int.find(e[1]) == node_to_int.end())
              node_to_int[e[1]] = node_count++;
          }

          UnionFind uf(num_nodes);

          // Shuffle edges.
          std::vector<Edge> copy_edges = edges;
          std::random_device rd;
          std::mt19937 g(rd());
          std::shuffle(copy_edges.begin(), copy_edges.end(), g);

          for (const auto& e : copy_edges)
          {
            int u = node_to_int[e[0]], v = node_to_int[e[1]];
            if (!uf.connected(u, v)) 
            {
                uf.unionSets(u, v);
                mst.push_back(e);
            }
          }

          return mst; 
        });
}
