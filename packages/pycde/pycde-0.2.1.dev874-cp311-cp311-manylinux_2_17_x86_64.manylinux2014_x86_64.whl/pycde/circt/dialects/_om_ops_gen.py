
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import extend_opview_class as _ods_extend_opview_class, segmented_accessor as _ods_segmented_accessor, equally_sized_accessor as _ods_equally_sized_accessor, get_default_loc_context as _ods_get_default_loc_context, get_op_result_or_value as _get_op_result_or_value, get_op_results_or_values as _get_op_results_or_values
_ods_ir = _ods_cext.ir

try:
  from . import _om_ops_ext as _ods_ext_module
except ImportError:
  _ods_ext_module = None

import builtins


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "om"
  pass


@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ClassFieldOp(_ods_ir.OpView):
  OPERATION_NAME = "om.class.field"

  _ODS_REGIONS = (0, True)

  def __init__(self, sym_name, value, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(value))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["sym_name"] = (sym_name if (
    issubclass(type(sym_name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(sym_name, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def value(self):
    return self.operation.operands[0]

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ClassOp(_ods_ir.OpView):
  OPERATION_NAME = "om.class"

  _ODS_REGIONS = (1, True)

  def __init__(self, sym_name, formalParamNames, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["sym_name"] = (sym_name if (
    issubclass(type(sym_name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(sym_name, context=_ods_context))
    attributes["formalParamNames"] = (formalParamNames if (
    issubclass(type(formalParamNames), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrArrayAttr')) else
      _ods_ir.AttrBuilder.get('StrArrayAttr')(formalParamNames, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ConstantOp(_ods_ir.OpView):
  OPERATION_NAME = "om.constant"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, value, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["value"] = (value if (
    issubclass(type(value), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('TypedAttrInterface')) else
      _ods_ir.AttrBuilder.get('TypedAttrInterface')(value, context=_ods_context))
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ObjectFieldOp(_ods_ir.OpView):
  OPERATION_NAME = "om.object.field"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, object, fieldPath, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(object))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["fieldPath"] = (fieldPath if (
    issubclass(type(fieldPath), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('FlatSymbolRefArrayAttr')) else
      _ods_ir.AttrBuilder.get('FlatSymbolRefArrayAttr')(fieldPath, context=_ods_context))
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def object(self):
    return self.operation.operands[0]

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ObjectOp(_ods_ir.OpView):
  OPERATION_NAME = "om.object"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, className, actualParams, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(actualParams))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["className"] = (className if (
    issubclass(type(className), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(className, context=_ods_context))
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def actualParams(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def className(self):
    return _ods_ir.StringAttr(self.operation.attributes["className"])

  @className.setter
  def className(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["className"] = value

  @builtins.property
  def result(self):
    return self.operation.results[0]
