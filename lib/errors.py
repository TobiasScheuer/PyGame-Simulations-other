class PlacementError(Exception):
	def __init__(self, machinetype, coordinates, entity):
		machine = str(machinetype)
		machine = machine.split('.')[1]
		machine = machine.split('\'')[0]
		print(f"Can't place {machine} at {coordinates}, because of {entity}")

class Other_Error(Exception):
	def __init__(self, machinetype, coordinates):
		machine = str(machinetype)
		machine = machine.split('.')[1]
		machine = machine.split('\'')[0]
		print(f"{machine} at {coordinates} has unspecified error")