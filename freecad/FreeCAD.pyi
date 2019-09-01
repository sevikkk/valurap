ActiveDocument: Document

def open(name: str): ...
def setActiveDocument(name: str): ...

class Document:
	def getObject(self, name: str) -> Obj: ...
	def removeObject(self, name: str) -> None: ...
	def addObject(self, type: str, name: str) -> Obj: ...
	def recompute(self) -> Obj: ...
	def saveAs(self, name: str) -> Obj: ...

class Obj:
	BaseFeature: object
	ViewObject: Union[None, ViewObject]
	Placement: Placement
	def removeObjectsFromDocument(self) -> None: ...

class Placement:
        Base: Vector
	def __init__(self, placement: Vector, rotation: Rotation) -> None: ...

class ViewOject:
	Visibility: bool

class Vector:
	def __init__(self,
		x: Union[float, int],
		y: Union[float, int],
		z: Union[float, int],
		) -> None: ...

class Rotation:
	def __init__(self,
		axe: Vector,
		angle: Union[float, int],
		) -> None: ...
