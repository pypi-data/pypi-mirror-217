# provides a convenient and streamlined approach to analyze Windows processes by converting windbg requests to pandas DataFrames

## pip install windbg2df

#### Tested against Windows 10 / Python 3.10 / Anaconda 


### Process analysis: 

It allows users to gather detailed information about a specific process, 
such as loaded modules, handles, and stack traces. This can help in diagnosing 
issues related to process behavior, resource utilization, or memory management.

### Memory region analysis: 

The module enables users to obtain information about specific memory regions within a process. 
This can be useful for identifying memory-related problems, analyzing memory usage patterns, 
or investigating memory leaks.

###  Memory category analysis: 

Users can retrieve information about memory categories using the module. 
This can provide insights into memory allocation patterns, such as the distribution 
of memory across different categories like heap, stack, or virtual memory.

### Integration with external tools: 

The module integrates with tools like 
procdump.exe https://download.sysinternals.com/files/Procdump.zip 
and kd.exe (WinDbg CLI) https://go.microsoft.com/fwlink/?linkid=2237510 
to perform analysis tasks. This allows users 
to leverage the capabilities of these powerful tools without 
directly interacting with them, simplifying the analysis process.

### Data exploration: 

The module returns analysis results in the form of pandas DataFrames, making it 
convenient to manipulate, filter, and visualize the gathered data. 
This facilitates exploratory data analysis and enables users to extract insights efficiently.


```python
     |  ProcDumpAnalyzer(pid, kd_exe='kd.exe', procdump_exe='procdump.exe')
     |  
     |  Class for analyzing process dumps using ProcDump and WinDbg.
     |  
     |  Args:
     |      pid (int): Process ID of the target process.
     |      kd_exe (str): Path to the kd.exe executable. Default is "kd.exe".
     |      procdump_exe (str): Path to the procdump.exe executable. Default is "procdump.exe".
     |  
     |  Attributes:
     |      kd_exe (str): Path to the kd.exe executable.
     |      procdump_exe (str): Path to the procdump.exe executable.
     |      pid (int): Process ID of the target process.
     |      fi: File information object for the process dump.
     |  
     |  Methods:
     |      get_procdump(): Retrieves the process dump using ProcDump and sets the file information.
     |      delete_all_tmp_files(): Deletes all temporary files generated during analysis.
     |      get_lmu_df(): Retrieves the loaded module information from the process dump as a DataFrame.
     |      get_handle_df(): Retrieves the handle information from the process dump as a DataFrame.
     |      get_kv_df(): Retrieves the call stack information from the process dump as a DataFrame.
     |      get_memory_region_df(start_address, end_address): Retrieves the memory region information from the process dump
     |          for the specified address range as a DataFrame.
     |      get_memory_cats_df(): Retrieves the memory categorization information from the process dump as a DataFrame.
     |  
     |  Example:
     |  from windbg2df import ProcDumpAnalyzer
     |  pro = ProcDumpAnalyzer(
     |  pid=12704,
     |  kd_exe=r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\kd.exe",
     |  procdump_exe=r"procdump.exe",
     |  ).delete_all_tmp_files().get_procdump()
     |  dflmu = pro.get_lmu_df()
     |  dfhandle = pro.get_handle_df()
     |  dfkv = pro.get_kv_df()
     |  start_address = "00007ff6`1b010000"
     |  end_address = "00007ff6`1b042000"
     |  df = pro.get_memory_region_df(start_address=start_address, end_address=end_address)
     |  dfmem = pro.get_memory_cats_df()
     |  
     |  print(dflmu[:20].to_string())
     |  print(dfhandle[:20].to_string())
     |  print(dfkv[:20].to_string())
     |  print(df[:20].to_string())
     |  print(dfmem[:20].to_string())
     |  
     |  # Output (notepad.exe)
     |  # 0            aa_start             aa_end                   aa_module_name
     |  # 0   00007ff6`1b010000  00007ff6`1b042000            notepad    (deferred)
     |  # 1   00007ffa`67cc0000  00007ffa`67d98000            efswrt     (deferred)
     |  # 2   00007ffa`70ef0000  00007ffa`71174000            comctl32   (deferred)
     |  # 3   00007ffa`71af0000  00007ffa`71b55000            oleacc     (deferred)
     |  # 4   00007ffa`7ae00000  00007ffa`7b0a7000            iertutil   (deferred)
     |  # 5   00007ffa`824c0000  00007ffa`8255b000  TextInputFramework   (deferred)
     |  # 6   00007ffa`833c0000  00007ffa`834d2000            MrmCoreR   (deferred)
     |  # 7   00007ffa`85d80000  00007ffa`85d9b000            mpr        (deferred)
     |  # 8   00007ffa`8e950000  00007ffa`8ec7a000    CoreUIComponents   (deferred)
     |  # 9   00007ffa`8f900000  00007ffa`8fa52000            WinTypes   (deferred)
     |  # 10  00007ffa`91830000  00007ffa`91904000       CoreMessaging   (deferred)
     |  # 11  00007ffa`91c70000  00007ffa`91d09000            uxtheme    (deferred)
     |  # 12  00007ffa`91ec0000  00007ffa`9211a000     twinapi_appcore   (deferred)
     |  # 13  00007ffa`92250000  00007ffa`92279000            rmclient   (deferred)
     |  # 14  00007ffa`92f30000  00007ffa`92f61000            ntmarta    (deferred)
     |  # 15  00007ffa`93ef0000  00007ffa`93f00000            umpdc      (deferred)
     |  # 16  00007ffa`93f00000  00007ffa`93f1e000            profapi    (deferred)
     |  # 17  00007ffa`93f20000  00007ffa`93f6a000            powrprof   (deferred)
     |  # 18  00007ffa`93f70000  00007ffa`93f81000      kernel_appcore   (deferred)
     |  # 19  00007ffa`93fb0000  00007ffa`94031000    bcryptPrimitives   (deferred)
     |  
     |  
     |  
     |  # 0             Handle                  Type
     |  # 0   0000000000000004                 Event
     |  # 1   0000000000000008                 Event
     |  # 2   000000000000000c  WaitCompletionPacket
     |  # 3   0000000000000010          IoCompletion
     |  # 4   0000000000000014       TpWorkerFactory
     |  # 5   0000000000000018               IRTimer
     |  # 6   000000000000001c  WaitCompletionPacket
     |  # 7   0000000000000020               IRTimer
     |  # 8   0000000000000024  WaitCompletionPacket
     |  # 9   0000000000000028
     |  # 10  000000000000002c
     |  # 11  0000000000000030
     |  # 12  0000000000000034             Directory
     |  # 13  0000000000000038                 Event
     |  # 14  000000000000003c                 Event
     |  # 15  0000000000000040                  File
     |  # 16  0000000000000044
     |  # 17  0000000000000048
     |  # 18  000000000000004c             ALPC Port
     |  # 19  0000000000000050
     |  
     |  
     |  
     |  # 0           Child-SP            RetAddr                                                            Args to Child                          Call Site
     |  # 0  000000e0`ed4af6a8  00007ffa`95df3a5d  00000000`00000000 00000000`00000000 0000b99e`00000000 00007ff6`00000001       win32u!NtUserGetMessage+0x14
     |  # 1  000000e0`ed4af6b0  00007ff6`1b01a3e3  00007ff6`1b010000 00000000`0003085c 00000000`00000000 00000000`00000000            user32!GetMessageW+0x2d
     |  # 2  000000e0`ed4af710  00007ff6`1b030347  000001fb`a1e245c0 000001fb`a1e245c2 00000000`00000000 00000000`00000000              notepad!WinMain+0x293
     |  # 3  000000e0`ed4af7e0  00007ffa`96527c24  00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000     notepad!__mainCRTStartup+0x19f
     |  # 4  000000e0`ed4af8a0  00007ffa`970ad721  00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000  kernel32!BaseThreadInitThunk+0x14
     |  # 5  000000e0`ed4af8d0  00000000`00000000  00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000      ntdll!RtlUserThreadStart+0x21
     |  
     |  
     |  
     |  #    aa_address1_hex_block aa_address2_hex_block aa_address_int_block   aa_address_sub      aa_whole_string  aa_Byte_int  aa_2Bytes_int  aa_4Bytes_int        aa_8Bytes_int  aa_4Bytes_float  aa_8Bytes_float aa_string
     |  # 0               00007ff6              1b010000      140694991732736  140694991732736  b'MZ..............'           77          19789     1296911693  2111428794711362893     2.152747e+08    1.552849e-167      b'M'
     |  # 1               00007ff6              1b010000      140694991732736  140694991732737  b'MZ..............'           90          23130     1515870810  2187159913151224410     1.536522e+16    1.830507e-162      b'Z'
     |  # 2               00007ff6              1b010000      140694991732736  140694991732738  b'MZ..............'          144          37008     2425393296  2634764732586823824    -5.702072e-29    1.458565e-132   b'\x90'
     |  # 3               00007ff6              1b010000      140694991732736  140694991732739  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 4               00007ff6              1b010000      140694991732736  140694991732740  b'MZ..............'            3            771       50529027   217020518514230019     3.850090e-37    3.720974e-294   b'\x03'
     |  # 5               00007ff6              1b010000      140694991732736  140694991732741  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 6               00007ff6              1b010000      140694991732736  140694991732742  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 7               00007ff6              1b010000      140694991732736  140694991732743  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 8               00007ff6              1b010000      140694991732736  140694991732744  b'MZ..............'           64          16448     1077952576  1171006547816366144     3.003922e+00    2.093500e-230      b'@'
     |  # 9               00007ff6              1b010000      140694991732736  140694991732745  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 10              00007ff6              1b010000      140694991732736  140694991732746  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 11              00007ff6              1b010000      140694991732736  140694991732747  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 12              00007ff6              1b010000      140694991732736  140694991732748  b'MZ..............'          255          65535     4294967295  5476377146882523135              NaN     1.255420e+58   b'\xff'
     |  # 13              00007ff6              1b010000      140694991732736  140694991732749  b'MZ..............'          255          65535     4294967295  5476377146882523135              NaN     1.255420e+58   b'\xff'
     |  # 14              00007ff6              1b010000      140694991732736  140694991732750  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 15              00007ff6              1b010000      140694991732736  140694991732751  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 16              00007ff6              1b010010      140694991732752  140694991732752  b'........@.......'          184          47288     3099113656  3798989389199620280    -8.808210e-05     1.008224e-54   b'\xb8'
     |  # 17              00007ff6              1b010010      140694991732752  140694991732753  b'........@.......'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 18              00007ff6              1b010010      140694991732752  140694991732754  b'........@.......'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  # 19              00007ff6              1b010010      140694991732752  140694991732755  b'........@.......'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
     |  
     |  
     |  # 0  aa_ aa_BaseAddress aa_EndAddress_1 aa_RegionSize      aa_Type     aa_State                   aa_Protect                                                     aa_Usage
     |  # 0    +     0`00000000      0`21c40000    0`21c40000                  MEM_FREE                                                                                      Free
     |  # 1    +     0`21c40000      0`21c41000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             <unknown>  [2..........J....]
     |  # 2    +     0`21c41000      0`21c50000    0`0000f000                  MEM_FREE                                                                                      Free
     |  # 3    +     0`21c50000      0`21c51000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             <unknown>  [0..........J....]
     |  # 4    +     0`21c51000      0`7ffe0000    0`5e38f000                  MEM_FREE                                                                                      Free
     |  # 5    +     0`7ffe0000      0`7ffe1000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             Other      [User Shared Data]
     |  # 6    +     0`7ffe1000      0`7ffe3000    0`00002000                  MEM_FREE                                                                                      Free
     |  # 7    +     0`7ffe3000      0`7ffe4000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             <unknown>  [HalT.....9V..P..]
     |  # 8    +     0`7ffe4000     e0`ed430000   e0`6d44c000                  MEM_FREE                                                                                      Free
     |  # 9    +    e0`ed430000     e0`ed49c000    0`0006c000  MEM_PRIVATE  MEM_RESERVE                                                                 Stack      [~0; 31a0.514]
     |  # 10        e0`ed49c000     e0`ed49f000    0`00003000  MEM_PRIVATE   MEM_COMMIT  PAGE_READWRITE | PAGE_GUARD                                    Stack      [~0; 31a0.514]
     |  # 11        e0`ed49f000     e0`ed4b0000    0`00011000  MEM_PRIVATE   MEM_COMMIT                                                                 Stack      [~0; 31a0.514]
     |  # 12   +    e0`ed4b0000     e0`ed600000    0`00150000                  MEM_FREE                                                                                      Free
     |  # 13   +    e0`ed600000     e0`ed61c000    0`0001c000  MEM_PRIVATE  MEM_RESERVE                                                                                 <unknown>
     |  # 14        e0`ed61c000     e0`ed61d000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                                         PEB        [31a0]
     |  # 15        e0`ed61d000     e0`ed61f000    0`00002000  MEM_PRIVATE   MEM_COMMIT                                                                 TEB        [~0; 31a0.514]
     |  # 16        e0`ed61f000     e0`ed800000    0`001e1000  MEM_PRIVATE  MEM_RESERVE                                                                                 <unknown>
     |  # 17   +    e0`ed800000    1fb`a1c40000  11a`b4440000                  MEM_FREE                                                                                      Free
     |  # 18   +   1fb`a1c40000    1fb`a1c50000    0`00010000   MEM_MAPPED   MEM_COMMIT                               Heap       [ID: 1; Handle: 000001fba1c40000; Type: Segment]
     |  # 19   +   1fb`a1c50000    1fb`a1c54000    0`00004000   MEM_MAPPED   MEM_COMMIT                                                             <unknown>  [.........p...NB.]
     |  
     |  Methods defined here:
     |  
     |  __init__(self, pid, kd_exe='kd.exe', procdump_exe='procdump.exe')
     |      Initialize a ProcDumpAnalyzer object.
     |      
     |      Args:
     |          pid (int): The process ID to analyze.
     |          kd_exe (str): The path to the kd.exe executable (default is "kd.exe").
     |          procdump_exe (str): The path to the procdump.exe executable (default is "procdump.exe").
     |  
     |  delete_all_tmp_files(self)
     |      Delete all temporary files.
     |      
     |      Returns:
     |          ProcDumpAnalyzer: The ProcDumpAnalyzer object.
     |  
     |  get_handle_df(self)
     |      Get the handle information as a DataFrame.
     |      
     |      Returns:
     |          pd.DataFrame: The DataFrame containing the handle information.
     |  
     |  get_kv_df(self)
     |      Get the stack trace information as a DataFrame.
     |      
     |      Returns:
     |          pd.DataFrame: The DataFrame containing the stack trace information.
     |  
     |  get_lmu_df(self)
     |      Get the LMU (Loaded Module List) as a DataFrame.
     |      
     |      Returns:
     |          pd.DataFrame: The DataFrame containing the LMU information.
     |  
     |  get_memory_cats_df(self)
     |      Get the memory categories information as a DataFrame.
     |      
     |      Returns:
     |          pd.DataFrame: The DataFrame containing the memory categories information.
     |  
     |  get_memory_region_df(self, start_address, end_address)
     |      Get the memory region information as a DataFrame for the specified address range.
     |      
     |      Args:
     |          start_address (str): The start address of the memory region.
     |          end_address (str): The end address of the memory region.
     |      
     |      Returns:
     |          pd.DataFrame: The DataFrame containing the memory region information.
     |  
     |  get_procdump(self)
     |      Get the procdump file for the specified process ID.
     |      
     |      Returns:
     |          ProcDumpAnalyzer: The ProcDumpAnalyzer object.
```