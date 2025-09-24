[Click here](../README.md) to view the README.

## Design and implementation

The design of this application is minimalistic to get started with code examples on PSOC&trade; Edge MCU devices. All PSOC&trade; Edge E84 MCU applications have a dual-CPU three-project structure to develop code for the CM33 and CM55 cores. The CM33 core has two separate projects for the secure processing environment (SPE) and non-secure processing environment (NSPE). A project folder consists of various subfolders, each denoting a specific aspect of the project. The three project folders are as follows:

**Table 1. Application projects**

Project | Description
--------|------------------------
*proj_cm33_s* | Project for CM33 secure processing environment (SPE)
*proj_cm33_ns* | Project for CM33 non-secure processing environment (NSPE)
*proj_cm55* | CM55 project

<br>

In this code example, at device reset, the secured boot process starts from the ROM boot with the secured enclave (SE) as the root of trust (RoT). From the secured enclave, the boot flow is passed on to the system CPU subsystem where the secure CM33 application starts. After all necessary secure configurations, the flow is passed on to the non-secure CM33 application. Resource initialization for this example is performed by this CM33 non-secure project. It configures the system clocks, pins, clock to peripheral connections, and other platform resources. It then enables the CM55 core using the `Cy_SysEnableCM55()` function and the CM55 core is subsequently put to DeepSleep mode.

In the CM33 non-secure application, the clocks and system resources are initialized by the BSP initialization function. The retarget-io middleware is configured to use the debug UART, a user button is initialized and a task called "network task" is created and the RTOS scheduler starts. The rest of the application code is provided in the *secure_tcp_server.c* file and the keys and other macros are defined in the network *credentials.h* and *secure_tcp_server.h* files.

The *python-tcp-secure-client* provided in the project root folder contains the keys and certificates for the client and a python implementation of a simple secure TCP client.

In this example, the TCP server establishes a secure connection with the TCP client through an SSL handshake. During the SSL handshake, the server presents its SSL certificate for verification, and verifies the incoming client identity. The server's SSL certificate used in this example is a self-signed SSL certificate. See the [Creating a self-signed certificate](../README.md/#creating-a-self-signed-ssl-certificate) section for more details.

Once the SSL handshake completes successfully, the server allows you to send LED ON/OFF commands to the TCP client; the client responds by sending an acknowledgement message to the server.
