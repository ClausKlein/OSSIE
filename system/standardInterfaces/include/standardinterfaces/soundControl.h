// This file is generated by omniidl (C++ backend)- omniORB_4_1. Do not edit.
#ifndef __soundControl_hh__
#define __soundControl_hh__

#ifndef __CORBA_H_EXTERNAL_GUARD__
#include <omniORB4/CORBA.h>
#endif

#ifndef  USE_stub_in_nt_dll
# define USE_stub_in_nt_dll_NOT_DEFINED_soundControl
#endif
#ifndef  USE_core_stub_in_nt_dll
# define USE_core_stub_in_nt_dll_NOT_DEFINED_soundControl
#endif
#ifndef  USE_dyn_stub_in_nt_dll
# define USE_dyn_stub_in_nt_dll_NOT_DEFINED_soundControl
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

#ifndef __standardInterfaces_maudioInControl__
#define __standardInterfaces_maudioInControl__

  class audioInControl;
  class _objref_audioInControl;
  class _impl_audioInControl;
  
  typedef _objref_audioInControl* audioInControl_ptr;
  typedef audioInControl_ptr audioInControlRef;

  class audioInControl_Helper {
  public:
    typedef audioInControl_ptr _ptr_type;

    static _ptr_type _nil();
    static _CORBA_Boolean is_nil(_ptr_type);
    static void release(_ptr_type);
    static void duplicate(_ptr_type);
    static void marshalObjRef(_ptr_type, cdrStream&);
    static _ptr_type unmarshalObjRef(cdrStream&);
  };

  typedef _CORBA_ObjRef_Var<_objref_audioInControl, audioInControl_Helper> audioInControl_var;
  typedef _CORBA_ObjRef_OUT_arg<_objref_audioInControl,audioInControl_Helper > audioInControl_out;

#endif

  // interface audioInControl
  class audioInControl {
  public:
    // Declarations for this interface type.
    typedef audioInControl_ptr _ptr_type;
    typedef audioInControl_var _var_type;

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

    static _core_attr const char* _PD_repoId;

    // Other IDL defined within this scope.
    
  };

  class _objref_audioInControl :
    public virtual ::CORBA::Object,
    public virtual omniObjRef
  {
  public:
    

    inline _objref_audioInControl()  { _PR_setobj(0); }  // nil
    _objref_audioInControl(omniIOR*, omniIdentity*);

  protected:
    virtual ~_objref_audioInControl();

    
  private:
    virtual void* _ptrToObjRef(const char*);

    _objref_audioInControl(const _objref_audioInControl&);
    _objref_audioInControl& operator = (const _objref_audioInControl&);
    // not implemented

    friend class audioInControl;
  };

  class _pof_audioInControl : public _OMNI_NS(proxyObjectFactory) {
  public:
    inline _pof_audioInControl() : _OMNI_NS(proxyObjectFactory)(audioInControl::_PD_repoId) {}
    virtual ~_pof_audioInControl();

    virtual omniObjRef* newObjRef(omniIOR*,omniIdentity*);
    virtual _CORBA_Boolean is_a(const char*) const;
  };

  class _impl_audioInControl :
    public virtual omniServant
  {
  public:
    virtual ~_impl_audioInControl();

    
    
  public:  // Really protected, workaround for xlC
    virtual _CORBA_Boolean _dispatch(omniCallHandle&);

  private:
    virtual void* _ptrToInterface(const char*);
    virtual const char* _mostDerivedRepoId();
    
  };


  _CORBA_MODULE_VAR _dyn_attr const ::CORBA::TypeCode_ptr _tc_audioInControl;

#ifndef __standardInterfaces_maudioOutControl__
#define __standardInterfaces_maudioOutControl__

  class audioOutControl;
  class _objref_audioOutControl;
  class _impl_audioOutControl;
  
  typedef _objref_audioOutControl* audioOutControl_ptr;
  typedef audioOutControl_ptr audioOutControlRef;

  class audioOutControl_Helper {
  public:
    typedef audioOutControl_ptr _ptr_type;

    static _ptr_type _nil();
    static _CORBA_Boolean is_nil(_ptr_type);
    static void release(_ptr_type);
    static void duplicate(_ptr_type);
    static void marshalObjRef(_ptr_type, cdrStream&);
    static _ptr_type unmarshalObjRef(cdrStream&);
  };

  typedef _CORBA_ObjRef_Var<_objref_audioOutControl, audioOutControl_Helper> audioOutControl_var;
  typedef _CORBA_ObjRef_OUT_arg<_objref_audioOutControl,audioOutControl_Helper > audioOutControl_out;

#endif

  // interface audioOutControl
  class audioOutControl {
  public:
    // Declarations for this interface type.
    typedef audioOutControl_ptr _ptr_type;
    typedef audioOutControl_var _var_type;

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

    static _core_attr const char* _PD_repoId;

    // Other IDL defined within this scope.
    
  };

  class _objref_audioOutControl :
    public virtual ::CORBA::Object,
    public virtual omniObjRef
  {
  public:
    

    inline _objref_audioOutControl()  { _PR_setobj(0); }  // nil
    _objref_audioOutControl(omniIOR*, omniIdentity*);

  protected:
    virtual ~_objref_audioOutControl();

    
  private:
    virtual void* _ptrToObjRef(const char*);

    _objref_audioOutControl(const _objref_audioOutControl&);
    _objref_audioOutControl& operator = (const _objref_audioOutControl&);
    // not implemented

    friend class audioOutControl;
  };

  class _pof_audioOutControl : public _OMNI_NS(proxyObjectFactory) {
  public:
    inline _pof_audioOutControl() : _OMNI_NS(proxyObjectFactory)(audioOutControl::_PD_repoId) {}
    virtual ~_pof_audioOutControl();

    virtual omniObjRef* newObjRef(omniIOR*,omniIdentity*);
    virtual _CORBA_Boolean is_a(const char*) const;
  };

  class _impl_audioOutControl :
    public virtual omniServant
  {
  public:
    virtual ~_impl_audioOutControl();

    
    
  public:  // Really protected, workaround for xlC
    virtual _CORBA_Boolean _dispatch(omniCallHandle&);

  private:
    virtual void* _ptrToInterface(const char*);
    virtual const char* _mostDerivedRepoId();
    
  };


  _CORBA_MODULE_VAR _dyn_attr const ::CORBA::TypeCode_ptr _tc_audioOutControl;

_CORBA_MODULE_END



_CORBA_MODULE POA_standardInterfaces
_CORBA_MODULE_BEG

  class audioInControl :
    public virtual standardInterfaces::_impl_audioInControl,
    public virtual ::PortableServer::ServantBase
  {
  public:
    virtual ~audioInControl();

    inline ::standardInterfaces::audioInControl_ptr _this() {
      return (::standardInterfaces::audioInControl_ptr) _do_this(::standardInterfaces::audioInControl::_PD_repoId);
    }
  };

  class audioOutControl :
    public virtual standardInterfaces::_impl_audioOutControl,
    public virtual ::PortableServer::ServantBase
  {
  public:
    virtual ~audioOutControl();

    inline ::standardInterfaces::audioOutControl_ptr _this() {
      return (::standardInterfaces::audioOutControl_ptr) _do_this(::standardInterfaces::audioOutControl::_PD_repoId);
    }
  };

_CORBA_MODULE_END



_CORBA_MODULE OBV_standardInterfaces
_CORBA_MODULE_BEG

_CORBA_MODULE_END





#undef _core_attr
#undef _dyn_attr

void operator<<=(::CORBA::Any& _a, standardInterfaces::audioInControl_ptr _s);
void operator<<=(::CORBA::Any& _a, standardInterfaces::audioInControl_ptr* _s);
_CORBA_Boolean operator>>=(const ::CORBA::Any& _a, standardInterfaces::audioInControl_ptr& _s);

void operator<<=(::CORBA::Any& _a, standardInterfaces::audioOutControl_ptr _s);
void operator<<=(::CORBA::Any& _a, standardInterfaces::audioOutControl_ptr* _s);
_CORBA_Boolean operator>>=(const ::CORBA::Any& _a, standardInterfaces::audioOutControl_ptr& _s);



inline void
standardInterfaces::audioInControl::_marshalObjRef(::standardInterfaces::audioInControl_ptr obj, cdrStream& s) {
  omniObjRef::_marshal(obj->_PR_getobj(),s);
}


inline void
standardInterfaces::audioOutControl::_marshalObjRef(::standardInterfaces::audioOutControl_ptr obj, cdrStream& s) {
  omniObjRef::_marshal(obj->_PR_getobj(),s);
}




#ifdef   USE_stub_in_nt_dll_NOT_DEFINED_soundControl
# undef  USE_stub_in_nt_dll
# undef  USE_stub_in_nt_dll_NOT_DEFINED_soundControl
#endif
#ifdef   USE_core_stub_in_nt_dll_NOT_DEFINED_soundControl
# undef  USE_core_stub_in_nt_dll
# undef  USE_core_stub_in_nt_dll_NOT_DEFINED_soundControl
#endif
#ifdef   USE_dyn_stub_in_nt_dll_NOT_DEFINED_soundControl
# undef  USE_dyn_stub_in_nt_dll
# undef  USE_dyn_stub_in_nt_dll_NOT_DEFINED_soundControl
#endif

#endif  // __soundControl_hh__

