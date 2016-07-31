#!/usr/bin/python

import json
import os
import pygraphviz as pgv

def read_package_json(path):
   with open(path) as package_json:
      package_json_contents = json.load(package_json)
      return package_json_contents

def license_check(package_json_contents):
   license = ""

   if "license" in package_json_contents:
      license = package_json_contents["license"]
   elif "licenses" in package_json_contents:
      for l in package_json_contents["licenses"]:
         license += l["type"] + " "
   else:
      license = "WTF UNKNOWN"

   return license

def update_graph(graph, package_json_contents):
   module = package_json_contents["name"]
   for dependency in package_json_contents["dependencies"]:
      graph.add_edge(module, dependency)

def print_dependencies_info():
   dep_graph=pgv.AGraph()

   dep_graph=pgv.AGraph(strict=False,directed=True)
   dep_graph.graph_attr.update(rankdir="LR")

   for x in os.walk("node_modules"):
      path = x[0] + "/package.json"
      if not os.path.isfile(path):
         continue

      contents = read_package_json(path)

      name = contents["name"]
      description = contents["description"]
      license = license_check(contents)
      update_graph(dep_graph, contents)

      print name + " | " + description + " | " + license
   
   dep_graph.layout(prog="dot")   
   dep_graph.draw("dep_graph.png")

print_dependencies_info();
