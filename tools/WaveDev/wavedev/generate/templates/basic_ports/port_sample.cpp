__IN_PORT__::__IN_PORT__(__COMP_ARG__)
{
    __COMP_REF_DEF__
}

void __IN_PORT__::__OPERATION__

__OUT_PORT__::__OUT_PORT__(__COMP_ARG__)
{
    __COMP_REF_DEF__
}

void __OUT_PORT__::connectPort(CORBA::Object_ptr connection, const char *connectionId)
{
  __NAME_SPACE__::__INT_TYPE___var port = __NAME_SPACE__::__INT_TYPE__::_narrow(connection);
  outPorts.push_back(__OUT_PORT__::PortInfo(port,connectionId));
}

void __OUT_PORT__::disconnectPort(const char *connectionId)
{
  std::vector<__OUT_PORT__::PortInfo>::iterator i;

  for (i = outPorts.begin(); i != outPorts.end(); ++i) {
      if ((*i).connectionId == connectionId) {
          outPorts.erase(i);
          break;
      }
  }
}

std::vector<__OUT_PORT__::PortInfo> __OUT_PORT__::get_ports()
{
    return outPorts;
}

__ACE_SVC_DEF__

