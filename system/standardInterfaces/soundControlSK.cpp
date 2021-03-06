// This file is generated by omniidl (C++ backend)- omniORB_4_1. Do not edit.

#include "soundControl.h"
#include <omniORB4/IOP_S.h>
#include <omniORB4/IOP_C.h>
#include <omniORB4/callDescriptor.h>
#include <omniORB4/callHandle.h>
#include <omniORB4/objTracker.h>


OMNI_USING_NAMESPACE(omni)

static const char* _0RL_library_version = omniORB_4_1;



standardInterfaces::audioInControl_ptr standardInterfaces::audioInControl_Helper::_nil() {
  return ::standardInterfaces::audioInControl::_nil();
}

::CORBA::Boolean standardInterfaces::audioInControl_Helper::is_nil(::standardInterfaces::audioInControl_ptr p) {
  return ::CORBA::is_nil(p);

}

void standardInterfaces::audioInControl_Helper::release(::standardInterfaces::audioInControl_ptr p) {
  ::CORBA::release(p);
}

void standardInterfaces::audioInControl_Helper::marshalObjRef(::standardInterfaces::audioInControl_ptr obj, cdrStream& s) {
  ::standardInterfaces::audioInControl::_marshalObjRef(obj, s);
}

standardInterfaces::audioInControl_ptr standardInterfaces::audioInControl_Helper::unmarshalObjRef(cdrStream& s) {
  return ::standardInterfaces::audioInControl::_unmarshalObjRef(s);
}

void standardInterfaces::audioInControl_Helper::duplicate(::standardInterfaces::audioInControl_ptr obj) {
  if( obj && !obj->_NP_is_nil() )  omni::duplicateObjRef(obj);
}

standardInterfaces::audioInControl_ptr
standardInterfaces::audioInControl::_duplicate(::standardInterfaces::audioInControl_ptr obj)
{
  if( obj && !obj->_NP_is_nil() )  omni::duplicateObjRef(obj);
  return obj;
}

standardInterfaces::audioInControl_ptr
standardInterfaces::audioInControl::_narrow(::CORBA::Object_ptr obj)
{
  if( !obj || obj->_NP_is_nil() || obj->_NP_is_pseudo() ) return _nil();
  _ptr_type e = (_ptr_type) obj->_PR_getobj()->_realNarrow(_PD_repoId);
  return e ? e : _nil();
}


standardInterfaces::audioInControl_ptr
standardInterfaces::audioInControl::_unchecked_narrow(::CORBA::Object_ptr obj)
{
  if( !obj || obj->_NP_is_nil() || obj->_NP_is_pseudo() ) return _nil();
  _ptr_type e = (_ptr_type) obj->_PR_getobj()->_uncheckedNarrow(_PD_repoId);
  return e ? e : _nil();
}

standardInterfaces::audioInControl_ptr
standardInterfaces::audioInControl::_nil()
{
#ifdef OMNI_UNLOADABLE_STUBS
  static _objref_audioInControl _the_nil_obj;
  return &_the_nil_obj;
#else
  static _objref_audioInControl* _the_nil_ptr = 0;
  if( !_the_nil_ptr ) {
    omni::nilRefLock().lock();
    if( !_the_nil_ptr ) {
      _the_nil_ptr = new _objref_audioInControl;
      registerNilCorbaObject(_the_nil_ptr);
    }
    omni::nilRefLock().unlock();
  }
  return _the_nil_ptr;
#endif
}

const char* standardInterfaces::audioInControl::_PD_repoId = "IDL:standardInterfaces/audioInControl:1.0";


standardInterfaces::_objref_audioInControl::~_objref_audioInControl() {
  
}


standardInterfaces::_objref_audioInControl::_objref_audioInControl(omniIOR* ior, omniIdentity* id) :
   omniObjRef(::standardInterfaces::audioInControl::_PD_repoId, ior, id, 1)
   
   
{
  _PR_setobj(this);
}

void*
standardInterfaces::_objref_audioInControl::_ptrToObjRef(const char* id)
{
  if( id == ::standardInterfaces::audioInControl::_PD_repoId )
    return (::standardInterfaces::audioInControl_ptr) this;
  
  if( id == ::CORBA::Object::_PD_repoId )
    return (::CORBA::Object_ptr) this;

  if( omni::strMatch(id, ::standardInterfaces::audioInControl::_PD_repoId) )
    return (::standardInterfaces::audioInControl_ptr) this;
  
  if( omni::strMatch(id, ::CORBA::Object::_PD_repoId) )
    return (::CORBA::Object_ptr) this;

  return 0;
}

standardInterfaces::_pof_audioInControl::~_pof_audioInControl() {}


omniObjRef*
standardInterfaces::_pof_audioInControl::newObjRef(omniIOR* ior, omniIdentity* id)
{
  return new ::standardInterfaces::_objref_audioInControl(ior, id);
}


::CORBA::Boolean
standardInterfaces::_pof_audioInControl::is_a(const char* id) const
{
  if( omni::ptrStrMatch(id, ::standardInterfaces::audioInControl::_PD_repoId) )
    return 1;
  
  return 0;
}

const standardInterfaces::_pof_audioInControl _the_pof_standardInterfaces_maudioInControl;

standardInterfaces::_impl_audioInControl::~_impl_audioInControl() {}


::CORBA::Boolean
standardInterfaces::_impl_audioInControl::_dispatch(omniCallHandle& _handle)
{
  

  
  return 0;
}

void*
standardInterfaces::_impl_audioInControl::_ptrToInterface(const char* id)
{
  if( id == ::standardInterfaces::audioInControl::_PD_repoId )
    return (::standardInterfaces::_impl_audioInControl*) this;
  
  if( id == ::CORBA::Object::_PD_repoId )
    return (void*) 1;

  if( omni::strMatch(id, ::standardInterfaces::audioInControl::_PD_repoId) )
    return (::standardInterfaces::_impl_audioInControl*) this;
  
  if( omni::strMatch(id, ::CORBA::Object::_PD_repoId) )
    return (void*) 1;
  return 0;
}

const char*
standardInterfaces::_impl_audioInControl::_mostDerivedRepoId()
{
  return ::standardInterfaces::audioInControl::_PD_repoId;
}

standardInterfaces::audioOutControl_ptr standardInterfaces::audioOutControl_Helper::_nil() {
  return ::standardInterfaces::audioOutControl::_nil();
}

::CORBA::Boolean standardInterfaces::audioOutControl_Helper::is_nil(::standardInterfaces::audioOutControl_ptr p) {
  return ::CORBA::is_nil(p);

}

void standardInterfaces::audioOutControl_Helper::release(::standardInterfaces::audioOutControl_ptr p) {
  ::CORBA::release(p);
}

void standardInterfaces::audioOutControl_Helper::marshalObjRef(::standardInterfaces::audioOutControl_ptr obj, cdrStream& s) {
  ::standardInterfaces::audioOutControl::_marshalObjRef(obj, s);
}

standardInterfaces::audioOutControl_ptr standardInterfaces::audioOutControl_Helper::unmarshalObjRef(cdrStream& s) {
  return ::standardInterfaces::audioOutControl::_unmarshalObjRef(s);
}

void standardInterfaces::audioOutControl_Helper::duplicate(::standardInterfaces::audioOutControl_ptr obj) {
  if( obj && !obj->_NP_is_nil() )  omni::duplicateObjRef(obj);
}

standardInterfaces::audioOutControl_ptr
standardInterfaces::audioOutControl::_duplicate(::standardInterfaces::audioOutControl_ptr obj)
{
  if( obj && !obj->_NP_is_nil() )  omni::duplicateObjRef(obj);
  return obj;
}

standardInterfaces::audioOutControl_ptr
standardInterfaces::audioOutControl::_narrow(::CORBA::Object_ptr obj)
{
  if( !obj || obj->_NP_is_nil() || obj->_NP_is_pseudo() ) return _nil();
  _ptr_type e = (_ptr_type) obj->_PR_getobj()->_realNarrow(_PD_repoId);
  return e ? e : _nil();
}


standardInterfaces::audioOutControl_ptr
standardInterfaces::audioOutControl::_unchecked_narrow(::CORBA::Object_ptr obj)
{
  if( !obj || obj->_NP_is_nil() || obj->_NP_is_pseudo() ) return _nil();
  _ptr_type e = (_ptr_type) obj->_PR_getobj()->_uncheckedNarrow(_PD_repoId);
  return e ? e : _nil();
}

standardInterfaces::audioOutControl_ptr
standardInterfaces::audioOutControl::_nil()
{
#ifdef OMNI_UNLOADABLE_STUBS
  static _objref_audioOutControl _the_nil_obj;
  return &_the_nil_obj;
#else
  static _objref_audioOutControl* _the_nil_ptr = 0;
  if( !_the_nil_ptr ) {
    omni::nilRefLock().lock();
    if( !_the_nil_ptr ) {
      _the_nil_ptr = new _objref_audioOutControl;
      registerNilCorbaObject(_the_nil_ptr);
    }
    omni::nilRefLock().unlock();
  }
  return _the_nil_ptr;
#endif
}

const char* standardInterfaces::audioOutControl::_PD_repoId = "IDL:standardInterfaces/audioOutControl:1.0";


standardInterfaces::_objref_audioOutControl::~_objref_audioOutControl() {
  
}


standardInterfaces::_objref_audioOutControl::_objref_audioOutControl(omniIOR* ior, omniIdentity* id) :
   omniObjRef(::standardInterfaces::audioOutControl::_PD_repoId, ior, id, 1)
   
   
{
  _PR_setobj(this);
}

void*
standardInterfaces::_objref_audioOutControl::_ptrToObjRef(const char* id)
{
  if( id == ::standardInterfaces::audioOutControl::_PD_repoId )
    return (::standardInterfaces::audioOutControl_ptr) this;
  
  if( id == ::CORBA::Object::_PD_repoId )
    return (::CORBA::Object_ptr) this;

  if( omni::strMatch(id, ::standardInterfaces::audioOutControl::_PD_repoId) )
    return (::standardInterfaces::audioOutControl_ptr) this;
  
  if( omni::strMatch(id, ::CORBA::Object::_PD_repoId) )
    return (::CORBA::Object_ptr) this;

  return 0;
}

standardInterfaces::_pof_audioOutControl::~_pof_audioOutControl() {}


omniObjRef*
standardInterfaces::_pof_audioOutControl::newObjRef(omniIOR* ior, omniIdentity* id)
{
  return new ::standardInterfaces::_objref_audioOutControl(ior, id);
}


::CORBA::Boolean
standardInterfaces::_pof_audioOutControl::is_a(const char* id) const
{
  if( omni::ptrStrMatch(id, ::standardInterfaces::audioOutControl::_PD_repoId) )
    return 1;
  
  return 0;
}

const standardInterfaces::_pof_audioOutControl _the_pof_standardInterfaces_maudioOutControl;

standardInterfaces::_impl_audioOutControl::~_impl_audioOutControl() {}


::CORBA::Boolean
standardInterfaces::_impl_audioOutControl::_dispatch(omniCallHandle& _handle)
{
  

  
  return 0;
}

void*
standardInterfaces::_impl_audioOutControl::_ptrToInterface(const char* id)
{
  if( id == ::standardInterfaces::audioOutControl::_PD_repoId )
    return (::standardInterfaces::_impl_audioOutControl*) this;
  
  if( id == ::CORBA::Object::_PD_repoId )
    return (void*) 1;

  if( omni::strMatch(id, ::standardInterfaces::audioOutControl::_PD_repoId) )
    return (::standardInterfaces::_impl_audioOutControl*) this;
  
  if( omni::strMatch(id, ::CORBA::Object::_PD_repoId) )
    return (void*) 1;
  return 0;
}

const char*
standardInterfaces::_impl_audioOutControl::_mostDerivedRepoId()
{
  return ::standardInterfaces::audioOutControl::_PD_repoId;
}

POA_standardInterfaces::audioInControl::~audioInControl() {}

POA_standardInterfaces::audioOutControl::~audioOutControl() {}

