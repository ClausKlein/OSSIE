// This file is generated by omniidl (C++ backend) - omniORB_4_2. Do not edit.

#include "realFloat.h"

OMNI_USING_NAMESPACE(omni)

static const char* _0RL_dyn_library_version = omniORB_4_2_dyn;

static ::CORBA::TypeCode::_Tracker _0RL_tcTrack(__FILE__);

#if defined(HAS_Cplusplus_Namespace) && defined(_MSC_VER)
// MSVC++ does not give the constant external linkage otherwise.
namespace standardInterfaces { 
  const ::CORBA::TypeCode_ptr _tc_realFloat = CORBA::TypeCode::PR_interface_tc("IDL:standardInterfaces/realFloat:1.0", "realFloat", &_0RL_tcTrack);
} 
#else
const ::CORBA::TypeCode_ptr standardInterfaces::_tc_realFloat = CORBA::TypeCode::PR_interface_tc("IDL:standardInterfaces/realFloat:1.0", "realFloat", &_0RL_tcTrack);
#endif

static void _0RL_standardInterfaces_mrealFloat_marshal_fn(cdrStream& _s, void* _v)
{
  omniObjRef* _o = (omniObjRef*)_v;
  omniObjRef::_marshal(_o, _s);
}
static void _0RL_standardInterfaces_mrealFloat_unmarshal_fn(cdrStream& _s, void*& _v)
{
  omniObjRef* _o = omniObjRef::_unMarshal(standardInterfaces::realFloat::_PD_repoId, _s);
  _v = _o;
}
static void _0RL_standardInterfaces_mrealFloat_destructor_fn(void* _v)
{
  omniObjRef* _o = (omniObjRef*)_v;
  if (_o)
    omni::releaseObjRef(_o);
}

void operator<<=(::CORBA::Any& _a, standardInterfaces::realFloat_ptr _o)
{
  standardInterfaces::realFloat_ptr _no = standardInterfaces::realFloat::_duplicate(_o);
  _a.PR_insert(standardInterfaces::_tc_realFloat,
               _0RL_standardInterfaces_mrealFloat_marshal_fn,
               _0RL_standardInterfaces_mrealFloat_destructor_fn,
               _no->_PR_getobj());
}
void operator<<=(::CORBA::Any& _a, standardInterfaces::realFloat_ptr* _op)
{
  _a.PR_insert(standardInterfaces::_tc_realFloat,
               _0RL_standardInterfaces_mrealFloat_marshal_fn,
               _0RL_standardInterfaces_mrealFloat_destructor_fn,
               (*_op)->_PR_getobj());
  *_op = standardInterfaces::realFloat::_nil();
}

::CORBA::Boolean operator>>=(const ::CORBA::Any& _a, standardInterfaces::realFloat_ptr& _o)
{
  void* _v;
  if (_a.PR_extract(standardInterfaces::_tc_realFloat,
                    _0RL_standardInterfaces_mrealFloat_unmarshal_fn,
                    _0RL_standardInterfaces_mrealFloat_marshal_fn,
                    _0RL_standardInterfaces_mrealFloat_destructor_fn,
                    _v)) {
    omniObjRef* _r = (omniObjRef*)_v;
    if (_r)
      _o = (standardInterfaces::realFloat_ptr)_r->_ptrToObjRef(standardInterfaces::realFloat::_PD_repoId);
    else
      _o = standardInterfaces::realFloat::_nil();
    return 1;
  }
  return 0;
}

