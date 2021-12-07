// This file is generated by omniidl (C++ backend)- omniORB_4_2. Do not edit.
#ifndef __complexShort_hh__
#define __complexShort_hh__

#ifndef __CORBA_H_EXTERNAL_GUARD__
#include <omniORB4/CORBA.h>
#endif

#ifndef  USE_stub_in_nt_dll
# define USE_stub_in_nt_dll_NOT_DEFINED_complexShort
#endif
#ifndef  USE_core_stub_in_nt_dll
# define USE_core_stub_in_nt_dll_NOT_DEFINED_complexShort
#endif
#ifndef  USE_dyn_stub_in_nt_dll
# define USE_dyn_stub_in_nt_dll_NOT_DEFINED_complexShort
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

#ifndef __standardInterfaces_mcomplexShort__
#define __standardInterfaces_mcomplexShort__
  class complexShort;
  class _objref_complexShort;
  class _impl_complexShort;
  
  typedef _objref_complexShort* complexShort_ptr;
  typedef complexShort_ptr complexShortRef;

  class complexShort_Helper {
  public:
    typedef complexShort_ptr _ptr_type;

    static _ptr_type _nil();
    static _CORBA_Boolean is_nil(_ptr_type);
    static void release(_ptr_type);
    static void duplicate(_ptr_type);
    static void marshalObjRef(_ptr_type, cdrStream&);
    static _ptr_type unmarshalObjRef(cdrStream&);
  };

  typedef _CORBA_ObjRef_Var<_objref_complexShort, complexShort_Helper> complexShort_var;
  typedef _CORBA_ObjRef_OUT_arg<_objref_complexShort,complexShort_Helper > complexShort_out;

#endif

  // interface complexShort
  class complexShort {
  public:
    // Declarations for this interface type.
    typedef complexShort_ptr _ptr_type;
    typedef complexShort_var _var_type;

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

  class _objref_complexShort :
    public virtual ::CORBA::Object,
    public virtual omniObjRef
  {
  public:
    // IDL operations
    void pushPacket(const ::PortTypes::ShortSequence& I, const ::PortTypes::ShortSequence& Q);

    // Constructors
    inline _objref_complexShort()  { _PR_setobj(0); }  // nil
    _objref_complexShort(omniIOR*, omniIdentity*);

  protected:
    virtual ~_objref_complexShort();

    
  private:
    virtual void* _ptrToObjRef(const char*);

    _objref_complexShort(const _objref_complexShort&);
    _objref_complexShort& operator = (const _objref_complexShort&);
    // not implemented

    friend class complexShort;
  };

  class _pof_complexShort : public _OMNI_NS(proxyObjectFactory) {
  public:
    inline _pof_complexShort() : _OMNI_NS(proxyObjectFactory)(complexShort::_PD_repoId) {}
    virtual ~_pof_complexShort();

    virtual omniObjRef* newObjRef(omniIOR*,omniIdentity*);
    virtual _CORBA_Boolean is_a(const char*) const;
  };

  class _impl_complexShort :
    public virtual omniServant
  {
  public:
    virtual ~_impl_complexShort();

    virtual void pushPacket(const ::PortTypes::ShortSequence& I, const ::PortTypes::ShortSequence& Q) = 0;
    
  public:  // Really protected, workaround for xlC
    virtual _CORBA_Boolean _dispatch(omniCallHandle&);

  private:
    virtual void* _ptrToInterface(const char*);
    virtual const char* _mostDerivedRepoId();
    
  };


  _CORBA_MODULE_VAR _dyn_attr const ::CORBA::TypeCode_ptr _tc_complexShort;

_CORBA_MODULE_END



_CORBA_MODULE POA_standardInterfaces
_CORBA_MODULE_BEG

  class complexShort :
    public virtual standardInterfaces::_impl_complexShort,
    public virtual ::PortableServer::ServantBase
  {
  public:
    virtual ~complexShort();

    inline ::standardInterfaces::complexShort_ptr _this() {
      return (::standardInterfaces::complexShort_ptr) _do_this(::standardInterfaces::complexShort::_PD_repoId);
    }
  };

_CORBA_MODULE_END



_CORBA_MODULE OBV_standardInterfaces
_CORBA_MODULE_BEG

_CORBA_MODULE_END





#undef _core_attr
#undef _dyn_attr

void operator<<=(::CORBA::Any& _a, standardInterfaces::complexShort_ptr _s);
void operator<<=(::CORBA::Any& _a, standardInterfaces::complexShort_ptr* _s);
_CORBA_Boolean operator>>=(const ::CORBA::Any& _a, standardInterfaces::complexShort_ptr& _s);



inline void
standardInterfaces::complexShort::_marshalObjRef(::standardInterfaces::complexShort_ptr obj, cdrStream& s) {
  omniObjRef::_marshal(obj->_PR_getobj(),s);
}



#ifdef   USE_stub_in_nt_dll_NOT_DEFINED_complexShort
# undef  USE_stub_in_nt_dll
# undef  USE_stub_in_nt_dll_NOT_DEFINED_complexShort
#endif
#ifdef   USE_core_stub_in_nt_dll_NOT_DEFINED_complexShort
# undef  USE_core_stub_in_nt_dll
# undef  USE_core_stub_in_nt_dll_NOT_DEFINED_complexShort
#endif
#ifdef   USE_dyn_stub_in_nt_dll_NOT_DEFINED_complexShort
# undef  USE_dyn_stub_in_nt_dll
# undef  USE_dyn_stub_in_nt_dll_NOT_DEFINED_complexShort
#endif

#endif  // __complexShort_hh__

