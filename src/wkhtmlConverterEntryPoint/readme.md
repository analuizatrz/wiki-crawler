# HTML Converter Entry Point

Este é um projeto em java que disponibiliza acesso à biblioteca WikiModel para aplicações em python. Para tanto, é utilizada a bibliote p4j, em que um servidor é criado disponibilizando um gateway de acesso à API.

```
.
├── externalLibs
│   ├── bliki-core-3.0.19.jar
│   └── py4j-0.8.1.jar
├── HtmlConverterEntryPoint.jar
└── src
    └── core
        ├── Converter.java
        ├── EntryPoint.java
        └── Render.java

```
Nesta pasta há o código fonte (src), os compilador em .class (bin), as bibliotecas utilizadas (externalLibs) e um executável (HtmlConverterEntryPoint.jar). Para rodar o executável basta rodar no terminal:

```bash
java -jar HtmlConverterEntryPoint.jar
```

Para consumir a classe em python e converter um texto `md_wk_input` para `html_output`

```python
from py4j.java_gateway import JavaGateway

gateway = JavaGateway()

converter = gateway.entry_point.getConverter()
gateway.jvm.java.lang.System.out.println('Conectado !')

html_output = converter.convert(md_wk_input)
```