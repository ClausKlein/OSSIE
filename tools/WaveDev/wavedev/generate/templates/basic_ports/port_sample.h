// Declaration for provides ports
#ifndef __IN_CLASS___H
#define __IN_CLASS___H
class __IN_PORT__ : 
public POA___NAME_SPACE__::__INT_TYPE____ACE_INHERIT__
{
  public:
    __IN_PORT__(__COMP_ARG__);

    __OPERATION__

  private:
    __COMP_REF_DECL__
};
#endif

// Declaration for uses ports

#ifndef __OUT_CLASS___H
#define __OUT_CLASS___H
class __OUT_PORT__ : 
public virtual POA_CF::Port__ACE_INHERIT__
{
  public:
    __OUT_PORT__(__COMP_ARG__);
    void connectPort(CORBA::Object_ptr connection, const char* connectionId);
    void disconnectPort(const char* connectionId);
    __ACE_SVC_DECL__

    //Port Information Storage Class
    class PortInfo {
      public:
        PortInfo(__NAME_SPACE__::__INT_TYPE___var _port, const char *&_id)
        {
            port_var = _port;
            connectionId = _id;
        };

        PortInfo(const PortInfo &cp)
        {
            port_var = cp.port_var;
            connectionId = cp.connectionId;
        };

        __NAME_SPACE__::__INT_TYPE___var port_var;
        std::string connectionId;

      private:
        PortInfo(); //no default constructor
    };

    std::vector <__OUT_PORT__::PortInfo> get_ports();

  private:
    std::vector <__OUT_PORT__::PortInfo> outPorts;
    __COMP_REF_DECL__

};
#endif
