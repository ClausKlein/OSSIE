// This file is generated by omniidl (C++ backend)- omniORB_4_2. Do not edit.
#ifndef __realFloat_hh__
#define __realFloat_hh__

#ifndef __CORBA_H_EXTERNAL_GUARD__
#include <omniORB4/CORBA.h>
#endif

#ifndef  USE_stub_in_nt_dll
# define USE_stub_in_nt_dll_NOT_DEFINED_realFloat
#endif
#ifndef  USE_core_stub_in_nt_dll
# define USE_core_stub_in_nt_dll_NOT_DEFINED_realFloat
#endif
#ifndef  USE_dyn_stub_in_nt_dll
# define USE_dyn_stub_in_nt_dll_NOT_DEFINED_realFloat
#endif



#ifndef __PortTypes_hh_EXTERNAL_GUARD__
#define __PortTypes_hh_EXTERNAL_GUARD__
#include "ossie/PortTypes.h"
#endif



#ifdef USE_stub_in_nt_dll
# ifndef USE_core_stub_in_nt_dll
#  define USE_core_stub_in_nt_dll
# endif
# ifndef USE_dyn_stub_in_nt_dll
#  define USE_dyn_stub_in_nt_dll
# endif
#endif

#ifdef _core_attr
# error "A local CPP macro _core_attr has already been defined."
#else
# ifdef  USE_core_stub_in_nt_dll
#  define _core_attr _OMNIORB_NTDLL_IMPORT
# else
#  define _core_attr
# endif
#endif

#ifdef _dyn_attr
# error "A local CPP macro _dyn_attr has already been defined."
#else
# ifdef  USE_dyn_stub_in_nt_dll
#  define _dyn_attr _OMNIORB_NTDLL_IMPORT
# else
#  define _dyn_attr
# endif
#endif



_CORBA_MODULE standardInterfaces

_CORBA_MODULE_BEG

#ifndef __standardInterfaces_mrealFloat__
#define __standardInterfaces_mrealFloat__
  class realFloat;
  class _objref_realFloat;
  class _impl_realFloat;
  
  typedef _objref_realFloat* realFloat_ptr;
  typedef realFloat_ptr realFloatRef;

  class realFloat_Helper {
  public:
    typedef realFloat_ptr _ptr_type;

    static _ptr_type _nil();
    static _CORBA_Boolean is_nil(_ptr_type);
    static void release(_ptr_type);
    static void duplicate(_ptr_type);
    static void marshalObjRef(_ptr_type, cdrStream&);
    static _ptr_type unmarshalObjRef(cdrStream&);
  };

  typedef _CORBA_ObjRef_Var<_objref_realFloat, realFloat_Helper> realFloat_var;
  typedef _CORBA_ObjRef_OUT_arg<_objref_realFloat,realFloat_Helper > realFloat_out;

#endif

  // interface realFloat
  class realFloat {
  public:
    // Declarations for this interface type.
    typedef realFloat_ptr _ptr_type;
    typedef realFloat_var _var_type;

    static _ptr_type _duplicate(_ptr_type);
    static _ptr_type _narrow(::CORBA::Object_ptr);
    static _ptr_type _unchecked_narrow(::CORBA::Object_ptr);
    
    static _ptr_type _nil();

    static inline void _marshalObjRef(_ptr_type, cdrStream&);

    static inline _ptr_type _unmarshalObjRef(cdrStream& s) {
      omniObjRef* o = omniObjRef::_unMarshal(_PD_repoId,s);
      if (o)
        return (_ptr_type) o->_ptrToObjRef(_PD_repoId);
      else
        return _nil();
    }

    static inline _ptr_type _fromObjRef(omniObjRef* o) {
      if (o)
        return (_ptr_type) o->_ptrToObjRef(_PD_repoId);
      else
        return _nil();
    }

    static _core_attr const char* _PD_repoId;

    // Other IDL defined within this scope.
    
  };

  class _objref_realFloat :
    public virtual ::CORBA::Object,
    public virtual omniObjRef
  {
  public:
    // IDL operations
    void pushPacket(const ::PortTypes::FloatSequence& I);

    // Constructors
    inline _objref_realFloat()  { _PR_setobj(0); }  // nil
    _objref_realFloat(omniIOR*, omniIdentity*);

  protected:
    virtual ~_objref_realFloat();

    
  private:
    virtual void* _ptrToObjRef(const char*);

    _objref_realFloat(const _objref_realFloat&);
    _objref_realFloat& operator = (const _objref_realFloat&);
    // not implemented

    friend class realFloat;
  };

  class _pof_realFloat : public _OMNI_NS(proxyObjectFactory) {
  public:
    inline _pof_realFloat() : _OMNI_NS(proxyObjectFactory)(realFloat::_PD_repoId) {}
    virtual ~_pof_realFloat();

    virtual omniObjRef* newObjRef(omniIOR*,omniIdentity*);
    virtual _CORBA_Boolean is_a(const char*) const;
  };

  class _impl_realFloat :
    public virtual omniServant
  {
  public:
    virtual ~_impl_realFloat();

    virtual void pushPacket(const ::PortTypes::FloatSequence& I) = 0;
    
  public:  // Really protected, workaround for xlC
    virtual _CORBA_Boolean _dispatch(omniCallHandle&);

  private:
    virtual void* _ptrToInterface(const char*);
    virtual const char* _mostDerivedRepoId();
    
  };


  _CORBA_MODULE_VAR _dyn_attr const ::CORBA::TypeCode_ptr _tc_realFloat;

_CORBA_MODULE_END



_CORBA_MODULE POA_standardInterfaces
_CORBA_MODULE_BEG

  class realFloat :
    public virtual standardInterfaces::_impl_realFloat,
    public virtual ::PortableServer::ServantBase
  {
  public:
    virtual ~realFloat();

    inline ::standardInterfaces::realFloat_ptr _this() {
      return (::standardInterfaces::realFloat_ptr) _do_this(::standardInterfaces::realFloat::_PD_repoId);
    }
  };

_CORBA_MODULE_END



_CORBA_MODULE OBV_standardInterfaces
_CORBA_MODULE_BEG

_CORBA_MODULE_END





#undef _core_attr
#undef _dyn_attr

void operator<<=(::CORBA::Any& _a, standardInterfaces::realFloat_ptr _s);
void operator<<=(::CORBA::Any& _a, standardInterfaces::realFloat_ptr* _s);
_CORBA_Boolean operator>>=(const ::CORBA::Any& _a, standardInterfaces::realFloat_ptr& _s);



inline void
standardInterfaces::realFloat::_marshalObjRef(::standardInterfaces::realFloat_ptr obj, cdrStream& s) {
  omniObjRef::_marshal(obj->_PR_getobj(),s);
}



#ifdef   USE_stub_in_nt_dll_NOT_DEFINED_realFloat
# undef  USE_stub_in_nt_dll
# undef  USE_stub_in_nt_dll_NOT_DEFINED_realFloat
#endif
#ifdef   USE_core_stub_in_nt_dll_NOT_DEFINED_realFloat
# undef  USE_core_stub_in_nt_dll
# undef  USE_core_stub_in_nt_dll_NOT_DEFINED_realFloat
#endif
#ifdef   USE_dyn_stub_in_nt_dll_NOT_DEFINED_realFloat
# undef  USE_dyn_stub_in_nt_dll
# undef  USE_dyn_stub_in_nt_dll_NOT_DEFINED_realFloat
#endif

#endif  // __realFloat_hh__

