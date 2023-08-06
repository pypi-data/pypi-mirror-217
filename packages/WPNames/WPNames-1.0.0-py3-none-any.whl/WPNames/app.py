import requests

class WPNames:
	def __init__(self, target):
		self.target = target
		self.usersPath = "/wp-json/wp/v2/users"

	def getJsonData(self) -> dict:
		"""
		Returns data found in site, in JSON format.
		"""
		return requests.get(self.target+self.usersPath).json()

	def generateNamesYield(self):
		"""
		Yields usernames found on site.
		"""
		for x in self.getJsonData(): yield x['name']

	def generateNamesList(self) -> list:
		"""
		Returns usernames found on site, as a list.
		"""
		return [x['name'] for x in self.getJsonData()]


	def saveRawData(self, filename: str) -> None:
		"""
		Add a filename in the parameter. Executing this method will save all data in that filename.
		"""
		with open(filename, 'w') as f:
			f.write(getJsonData())
