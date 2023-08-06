<div align="center">
  
# WPNames
**WordPress Usernames Enumerator**

</div>

## Installation & Usage

Use the following command to install the tool.
```python
pip install WPNames
```
Then import the tool to any python file. Here's an example:

```py
from WPNames import WPNames

site = "https://example.com/"

WPNames(site).getJsonData()

```

## Methods

#### `getJsonData()` - retrives data from site in JSON format
#### `generateNamesYield()` - Yields usernames found on the site
#### `saveRawData('data.json')` - Saves the raw JSON data retrieved from the site. Make sure to replace `data.json` with desired filename
