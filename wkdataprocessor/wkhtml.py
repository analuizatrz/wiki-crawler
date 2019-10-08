from py4j.java_gateway import JavaGateway
import os

gateway = JavaGateway()

converter = gateway.entry_point.getConverter()

input_folder = "/home/ana/Downloads/input/"
titles = os.listdir(input_folder)
input = open(f"{input_folder}/{titles[0]}", "r").read()

gateway.jvm.java.lang.System.out.println('Hello World!')
html = converter.convert(input)
print(html)
