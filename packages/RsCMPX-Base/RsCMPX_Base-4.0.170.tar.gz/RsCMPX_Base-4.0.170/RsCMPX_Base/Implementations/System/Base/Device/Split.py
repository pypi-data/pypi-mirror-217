from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SplitCls:
	"""Split commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("split", core, parent)

	def set(self, count: int, direction: enums.DirectionHv) -> None:
		"""SCPI: SYSTem:BASE:DEVice:SPLit \n
		Snippet: driver.system.base.device.split.set(count = 1, direction = enums.DirectionHv.HORizontal) \n
		No command help available \n
			:param count: No help available
			:param direction: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('count', count, DataType.Integer), ArgSingle('direction', direction, DataType.Enum, enums.DirectionHv))
		self._core.io.write(f'SYSTem:BASE:DEVice:SPLit {param}'.rstrip())

	# noinspection PyTypeChecker
	class SplitStruct(StructBase):
		"""Response structure. Fields: \n
			- Count: int: No parameter help available
			- Direction: enums.DirectionHv: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Count'),
			ArgStruct.scalar_enum('Direction', enums.DirectionHv)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Count: int = None
			self.Direction: enums.DirectionHv = None

	def get(self) -> SplitStruct:
		"""SCPI: SYSTem:BASE:DEVice:SPLit \n
		Snippet: value: SplitStruct = driver.system.base.device.split.get() \n
		No command help available \n
			:return: structure: for return value, see the help for SplitStruct structure arguments."""
		return self._core.io.query_struct(f'SYSTem:BASE:DEVice:SPLit?', self.__class__.SplitStruct())
