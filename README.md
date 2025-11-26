# XML to JSON Conversion

Convert xml to json.

Usage: 
```shell
python main.py --xml input.xml --mapping mapping.json --json output.json
```

## Mapping

The mapping file defines how the output json file should be structured and where to find the data in the xml.
The keys represent the desired path in the output json.
The mapping file must be flat.
Nested JSON objects can be created by using dot notation (`.`). 
For example, a key `"general.ok"` will result in the following structure in the output JSON:
```json
{
  "general": {
    "ok": "..."
  }
}
```
The value should be XPath expressions to locate the corresponding element in the input XML file.
If an XPath expression does not find an element, the corresponding JSON property will have an empty string `""` as its value.
To create a key without a value it's also possible to leave the XPath expression empty.

## Example

A mapping file like this:
```json
{
  "culture": "./Meta[@type='culture']",
  "general.title": "./General/Title"
}
```
would with this xml file:
```xml
<Translations>
    <Meta type="culture">en-US</Meta>
    <Meta type="version">1.1</Meta>
    <General>
        <Title>My Application</Title>
    </General>
</Translations>
```
create this output:
```json
{
  "culture": "en-US",
  "general": {
    "title": "My Application"
  }
}
```
