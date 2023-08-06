import collections
import ctypes
import os
import subprocess
import sys
import tempfile
from ctypes.wintypes import HWND, COLORREF, BYTE, DWORD, BOOL
from functools import reduce
from math import ceil
from time import sleep, time
import gc
import kthread
import numexpr
import numpy as np
import regex
from PyPDump import ProcDump
from list_all_files_recursively import get_folder_file_complete_path
from ctypes_window_info import get_window_infos
import pandas as pd
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
from taskkill import taskkill_pid
from remtmp import delete_tmp_files

nested_dict = lambda: collections.defaultdict(nested_dict)
subconf = sys.modules[__name__]
subconf.allsubprocs = []
subconf.allsubprocs.append(None)
pd_add_apply_ignore_exceptions()
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
GWL_EXSTYLE = -20
WS_EX_LAYERED = ctypes.c_long(0x00080000)
LWA_ALPHA = DWORD(0x00000002)
crKey = COLORREF(0)
bAlpha = BYTE(0)
int_array = np.frompyfunc(int, 2, 1)

user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = BOOL
allindexchar = [21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66]
allhexnumbers = [
    b"0",
    b"1",
    b"2",
    b"3",
    b"4",
    b"5",
    b"6",
    b"7",
    b"8",
    b"9",
    b"a",
    b"b",
    b"c",
    b"d",
    b"e",
    b"f",
]
alldecnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
}


class ProcDumpAnalyzer:
    r"""
    Class for analyzing process dumps using ProcDump and WinDbg.

    Args:
        pid (int): Process ID of the target process.
        kd_exe (str): Path to the kd.exe executable. Default is "kd.exe".
        procdump_exe (str): Path to the procdump.exe executable. Default is "procdump.exe".

    Attributes:
        kd_exe (str): Path to the kd.exe executable.
        procdump_exe (str): Path to the procdump.exe executable.
        pid (int): Process ID of the target process.
        fi: File information object for the process dump.

    Methods:
        get_procdump(): Retrieves the process dump using ProcDump and sets the file information.
        delete_all_tmp_files(): Deletes all temporary files generated during analysis.
        get_lmu_df(): Retrieves the loaded module information from the process dump as a DataFrame.
        get_handle_df(): Retrieves the handle information from the process dump as a DataFrame.
        get_kv_df(): Retrieves the call stack information from the process dump as a DataFrame.
        get_memory_region_df(start_address, end_address): Retrieves the memory region information from the process dump
            for the specified address range as a DataFrame.
        get_memory_cats_df(): Retrieves the memory categorization information from the process dump as a DataFrame.

    Example:
    from windbg2df import ProcDumpAnalyzer
    pro = ProcDumpAnalyzer(
    pid=12704,
    kd_exe=r"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\kd.exe",
    procdump_exe=r"procdump.exe",
    ).delete_all_tmp_files().get_procdump()
    dflmu = pro.get_lmu_df()
    dfhandle = pro.get_handle_df()
    dfkv = pro.get_kv_df()
    start_address = "00007ff6`1b010000"
    end_address = "00007ff6`1b042000"
    df = pro.get_memory_region_df(start_address=start_address, end_address=end_address)
    dfmem = pro.get_memory_cats_df()

    print(dflmu[:20].to_string())
    print(dfhandle[:20].to_string())
    print(dfkv[:20].to_string())
    print(df[:20].to_string())
    print(dfmem[:20].to_string())

    # Output (notepad.exe)
    # 0            aa_start             aa_end                   aa_module_name
    # 0   00007ff6`1b010000  00007ff6`1b042000            notepad    (deferred)
    # 1   00007ffa`67cc0000  00007ffa`67d98000            efswrt     (deferred)
    # 2   00007ffa`70ef0000  00007ffa`71174000            comctl32   (deferred)
    # 3   00007ffa`71af0000  00007ffa`71b55000            oleacc     (deferred)
    # 4   00007ffa`7ae00000  00007ffa`7b0a7000            iertutil   (deferred)
    # 5   00007ffa`824c0000  00007ffa`8255b000  TextInputFramework   (deferred)
    # 6   00007ffa`833c0000  00007ffa`834d2000            MrmCoreR   (deferred)
    # 7   00007ffa`85d80000  00007ffa`85d9b000            mpr        (deferred)
    # 8   00007ffa`8e950000  00007ffa`8ec7a000    CoreUIComponents   (deferred)
    # 9   00007ffa`8f900000  00007ffa`8fa52000            WinTypes   (deferred)
    # 10  00007ffa`91830000  00007ffa`91904000       CoreMessaging   (deferred)
    # 11  00007ffa`91c70000  00007ffa`91d09000            uxtheme    (deferred)
    # 12  00007ffa`91ec0000  00007ffa`9211a000     twinapi_appcore   (deferred)
    # 13  00007ffa`92250000  00007ffa`92279000            rmclient   (deferred)
    # 14  00007ffa`92f30000  00007ffa`92f61000            ntmarta    (deferred)
    # 15  00007ffa`93ef0000  00007ffa`93f00000            umpdc      (deferred)
    # 16  00007ffa`93f00000  00007ffa`93f1e000            profapi    (deferred)
    # 17  00007ffa`93f20000  00007ffa`93f6a000            powrprof   (deferred)
    # 18  00007ffa`93f70000  00007ffa`93f81000      kernel_appcore   (deferred)
    # 19  00007ffa`93fb0000  00007ffa`94031000    bcryptPrimitives   (deferred)



    # 0             Handle                  Type
    # 0   0000000000000004                 Event
    # 1   0000000000000008                 Event
    # 2   000000000000000c  WaitCompletionPacket
    # 3   0000000000000010          IoCompletion
    # 4   0000000000000014       TpWorkerFactory
    # 5   0000000000000018               IRTimer
    # 6   000000000000001c  WaitCompletionPacket
    # 7   0000000000000020               IRTimer
    # 8   0000000000000024  WaitCompletionPacket
    # 9   0000000000000028
    # 10  000000000000002c
    # 11  0000000000000030
    # 12  0000000000000034             Directory
    # 13  0000000000000038                 Event
    # 14  000000000000003c                 Event
    # 15  0000000000000040                  File
    # 16  0000000000000044
    # 17  0000000000000048
    # 18  000000000000004c             ALPC Port
    # 19  0000000000000050



    # 0           Child-SP            RetAddr                                                            Args to Child                          Call Site
    # 0  000000e0`ed4af6a8  00007ffa`95df3a5d  00000000`00000000 00000000`00000000 0000b99e`00000000 00007ff6`00000001       win32u!NtUserGetMessage+0x14
    # 1  000000e0`ed4af6b0  00007ff6`1b01a3e3  00007ff6`1b010000 00000000`0003085c 00000000`00000000 00000000`00000000            user32!GetMessageW+0x2d
    # 2  000000e0`ed4af710  00007ff6`1b030347  000001fb`a1e245c0 000001fb`a1e245c2 00000000`00000000 00000000`00000000              notepad!WinMain+0x293
    # 3  000000e0`ed4af7e0  00007ffa`96527c24  00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000     notepad!__mainCRTStartup+0x19f
    # 4  000000e0`ed4af8a0  00007ffa`970ad721  00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000  kernel32!BaseThreadInitThunk+0x14
    # 5  000000e0`ed4af8d0  00000000`00000000  00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000      ntdll!RtlUserThreadStart+0x21



    #    aa_address1_hex_block aa_address2_hex_block aa_address_int_block   aa_address_sub      aa_whole_string  aa_Byte_int  aa_2Bytes_int  aa_4Bytes_int        aa_8Bytes_int  aa_4Bytes_float  aa_8Bytes_float aa_string
    # 0               00007ff6              1b010000      140694991732736  140694991732736  b'MZ..............'           77          19789     1296911693  2111428794711362893     2.152747e+08    1.552849e-167      b'M'
    # 1               00007ff6              1b010000      140694991732736  140694991732737  b'MZ..............'           90          23130     1515870810  2187159913151224410     1.536522e+16    1.830507e-162      b'Z'
    # 2               00007ff6              1b010000      140694991732736  140694991732738  b'MZ..............'          144          37008     2425393296  2634764732586823824    -5.702072e-29    1.458565e-132   b'\x90'
    # 3               00007ff6              1b010000      140694991732736  140694991732739  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 4               00007ff6              1b010000      140694991732736  140694991732740  b'MZ..............'            3            771       50529027   217020518514230019     3.850090e-37    3.720974e-294   b'\x03'
    # 5               00007ff6              1b010000      140694991732736  140694991732741  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 6               00007ff6              1b010000      140694991732736  140694991732742  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 7               00007ff6              1b010000      140694991732736  140694991732743  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 8               00007ff6              1b010000      140694991732736  140694991732744  b'MZ..............'           64          16448     1077952576  1171006547816366144     3.003922e+00    2.093500e-230      b'@'
    # 9               00007ff6              1b010000      140694991732736  140694991732745  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 10              00007ff6              1b010000      140694991732736  140694991732746  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 11              00007ff6              1b010000      140694991732736  140694991732747  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 12              00007ff6              1b010000      140694991732736  140694991732748  b'MZ..............'          255          65535     4294967295  5476377146882523135              NaN     1.255420e+58   b'\xff'
    # 13              00007ff6              1b010000      140694991732736  140694991732749  b'MZ..............'          255          65535     4294967295  5476377146882523135              NaN     1.255420e+58   b'\xff'
    # 14              00007ff6              1b010000      140694991732736  140694991732750  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 15              00007ff6              1b010000      140694991732736  140694991732751  b'MZ..............'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 16              00007ff6              1b010010      140694991732752  140694991732752  b'........@.......'          184          47288     3099113656  3798989389199620280    -8.808210e-05     1.008224e-54   b'\xb8'
    # 17              00007ff6              1b010010      140694991732752  140694991732753  b'........@.......'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 18              00007ff6              1b010010      140694991732752  140694991732754  b'........@.......'            0              0              0                    0     0.000000e+00     0.000000e+00       b''
    # 19              00007ff6              1b010010      140694991732752  140694991732755  b'........@.......'            0              0              0                    0     0.000000e+00     0.000000e+00       b''


    # 0  aa_ aa_BaseAddress aa_EndAddress_1 aa_RegionSize      aa_Type     aa_State                   aa_Protect                                                     aa_Usage
    # 0    +     0`00000000      0`21c40000    0`21c40000                  MEM_FREE                                                                                      Free
    # 1    +     0`21c40000      0`21c41000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             <unknown>  [2..........J....]
    # 2    +     0`21c41000      0`21c50000    0`0000f000                  MEM_FREE                                                                                      Free
    # 3    +     0`21c50000      0`21c51000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             <unknown>  [0..........J....]
    # 4    +     0`21c51000      0`7ffe0000    0`5e38f000                  MEM_FREE                                                                                      Free
    # 5    +     0`7ffe0000      0`7ffe1000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             Other      [User Shared Data]
    # 6    +     0`7ffe1000      0`7ffe3000    0`00002000                  MEM_FREE                                                                                      Free
    # 7    +     0`7ffe3000      0`7ffe4000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                             <unknown>  [HalT.....9V..P..]
    # 8    +     0`7ffe4000     e0`ed430000   e0`6d44c000                  MEM_FREE                                                                                      Free
    # 9    +    e0`ed430000     e0`ed49c000    0`0006c000  MEM_PRIVATE  MEM_RESERVE                                                                 Stack      [~0; 31a0.514]
    # 10        e0`ed49c000     e0`ed49f000    0`00003000  MEM_PRIVATE   MEM_COMMIT  PAGE_READWRITE | PAGE_GUARD                                    Stack      [~0; 31a0.514]
    # 11        e0`ed49f000     e0`ed4b0000    0`00011000  MEM_PRIVATE   MEM_COMMIT                                                                 Stack      [~0; 31a0.514]
    # 12   +    e0`ed4b0000     e0`ed600000    0`00150000                  MEM_FREE                                                                                      Free
    # 13   +    e0`ed600000     e0`ed61c000    0`0001c000  MEM_PRIVATE  MEM_RESERVE                                                                                 <unknown>
    # 14        e0`ed61c000     e0`ed61d000    0`00001000  MEM_PRIVATE   MEM_COMMIT                                                                         PEB        [31a0]
    # 15        e0`ed61d000     e0`ed61f000    0`00002000  MEM_PRIVATE   MEM_COMMIT                                                                 TEB        [~0; 31a0.514]
    # 16        e0`ed61f000     e0`ed800000    0`001e1000  MEM_PRIVATE  MEM_RESERVE                                                                                 <unknown>
    # 17   +    e0`ed800000    1fb`a1c40000  11a`b4440000                  MEM_FREE                                                                                      Free
    # 18   +   1fb`a1c40000    1fb`a1c50000    0`00010000   MEM_MAPPED   MEM_COMMIT                               Heap       [ID: 1; Handle: 000001fba1c40000; Type: Segment]
    # 19   +   1fb`a1c50000    1fb`a1c54000    0`00004000   MEM_MAPPED   MEM_COMMIT                                                             <unknown>  [.........p...NB.]
    """

    def __init__(self, pid, kd_exe="kd.exe", procdump_exe=r"procdump.exe"):
        """
        Initialize a ProcDumpAnalyzer object.

        Args:
            pid (int): The process ID to analyze.
            kd_exe (str): The path to the kd.exe executable (default is "kd.exe").
            procdump_exe (str): The path to the procdump.exe executable (default is "procdump.exe").
        """
        self.kd_exe = kd_exe
        self.procdump_exe = procdump_exe
        self.pid = pid
        self.fi = None

    def get_procdump(self):
        """
        Get the procdump file for the specified process ID.

        Returns:
            ProcDumpAnalyzer: The ProcDumpAnalyzer object.
        """
        self.fi = get_procdump(self.procdump_exe, pid=self.pid)
        return self

    def delete_all_tmp_files(self):
        """
        Delete all temporary files.

        Returns:
            ProcDumpAnalyzer: The ProcDumpAnalyzer object.
        """
        delete_tmp_files()
        return self

    def get_lmu_df(self):
        """
        Get the LMU (Loaded Module List) as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the LMU information.
        """
        return get_lmu_df(windbgexe=self.kd_exe, procfile=self.fi)

    def get_handle_df(self):
        """
        Get the handle information as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the handle information.
        """
        return get_handle_df(windbgexe=self.kd_exe, procfile=self.fi)

    def get_kv_df(self):
        """
        Get the stack trace information as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the stack trace information.
        """
        return get_kv_df(windbgexe=self.kd_exe, procfile=self.fi)

    def get_memory_region_df(self, start_address, end_address):
        """
        Get the memory region information as a DataFrame for the specified address range.

        Args:
            start_address (str): The start address of the memory region.
            end_address (str): The end address of the memory region.

        Returns:
            pd.DataFrame: The DataFrame containing the memory region information.
        """
        return get_df_from_mem_region(
            windbgexe=self.kd_exe,
            procfile=self.fi,
            start_address=start_address,
            end_address=end_address,
        )

    def get_memory_cats_df(self):
        """
        Get the memory categories information as a DataFrame.

        Returns:
            pd.DataFrame: The DataFrame containing the memory categories information.
        """
        data1 = get_windbg(
            command="!address",
            procfile=self.fi,
            windbexe=self.kd_exe,
        )
        return convert_windbg2df(data1, use_first_row_as_columns=True, dbcmd=False)


def tempfolder():
    tempfolder = tempfile.TemporaryDirectory()
    tempfolder.cleanup()
    if not os.path.exists(tempfolder.name):
        os.makedirs(tempfolder.name)

    return tempfolder.name


def is_file_being_used(f):
    if os.path.exists(f):
        try:
            os.rename(f, f)
            return False
        except OSError as e:
            return True
    return True


def execute_subp(command):
    subconf.allsubprocs.append(
        subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            bufsize=0,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **invisibledict,
        )
    )


def get_windbg(command, procfile, windbexe, timeout=5):
    mytempfolder = tempfolder()
    command = [
        windbexe,
        "-z",
        procfile,
        "-kqm",
        "-c",
        rf"sqe; .logopen /t {mytempfolder}\output.txt; {command.strip()}; .logclose; q",
    ]
    oldproc = subconf.allsubprocs[-1]
    t = kthread.KThread(target=execute_subp, name=str(command), args=(command,))
    t.start()
    while subconf.allsubprocs[-1] == oldproc:
        sleep(0.1)
    p = subconf.allsubprocs[-1]
    allvi = []
    timeoutfinal = time() + timeout
    checkalvi = False
    if checkalvi:
        while not allvi:
            if timeoutfinal < time():
                taskkill_pid(p.pid)
                return []
            allvi = [
                x
                for x in get_window_infos()
                if x.title == "WinBaseClass" and "windbg.exe" in x.path
            ]
        _handle = int(allvi[0].hwnd)
        hwnd = HWND(_handle)
        result = user32.MoveWindow(_handle, -100, -100, 101, 101, True)
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, WS_EX_LAYERED)
        user32.SetLayeredWindowAttributes(hwnd, crKey, 0, LWA_ALPHA)
        user32.UpdateWindow(hwnd)
    allfi = get_folder_file_complete_path(mytempfolder)
    timeoutfinal = time() + timeout
    while not allfi:
        if timeoutfinal < time():
            taskkill_pid(p.pid)

            return []
        allfi = get_folder_file_complete_path(mytempfolder)
        sleep(0.1)
    txtfile = allfi[0].path
    timeoutfinal = time() + timeout

    while is_file_being_used(txtfile):
        if timeoutfinal < time():
            taskkill_pid(p.pid)

            return []
        sleep(0.1)
    with open(txtfile, mode="rb") as f:
        data = f.read()
    data = [
        x
        for x in data.strip().splitlines()[1:-1]
        if (h := x.strip()) and h.count(b"-") != len(h)
    ]
    try:
        datatemp = (data[-1] + b" " * len(data[-2]))[: len(data[-2])]
        data = data[:-1]
        data.append(datatemp)

    except Exception as fa:
        pass
    try:
        os.remove(txtfile)
        os.removedirs(mytempfolder)
    except Exception:
        pass
    taskkill_pid(p.pid)

    return data


def convert_windbg2df(data, use_first_row_as_columns=False, dbcmd=False):
    if not data:
        return pd.DataFrame()
    sets = set(
        (
            frozenset(
                y.start()
                for y in (
                    regex.finditer(
                        b" ",
                        d,
                        concurrent=True,
                        partial=False,
                    )
                )
            )
            for d in data
        )
    )
    intersection = reduce(lambda x, y: x.intersection(y), sets)
    intersection = list(sorted(list(intersection)))
    intersectionarray = np.array(intersection)
    split_indices = intersectionarray[
        np.where(np.diff(intersectionarray) > 1)[0]
    ].tolist()
    split_indices.append(intersection[-1])
    char_array = np.char.array(data)
    maxlen = np.char.array(data).dtype.base.itemsize
    char_array = char_array.ljust(maxlen)
    char_array = char_array.view("S1").reshape((-1, maxlen))
    splits = np.array_split(char_array, split_indices, axis=1)
    splits = [x for x in splits if x[0].shape[0]]
    df = pd.concat(
        [
            pd.DataFrame(splits[r].view(f"S{len(splits[r][0])}"))
            for r in range(len(splits))
        ],
        axis=1,
        ignore_index=True,
    )
    for co in df.columns:
        df[co] = np.char.array(df[co].__array__()).strip().decode("utf-8", "ignore")
    if use_first_row_as_columns:
        df.columns = "aa_" + df.iloc[0].str.replace(r"\W", "_", regex=True).str.strip(
            "_"
        )
        df = df.drop(0)
    df = df.reset_index(drop=True)
    if dbcmd:
        df8 = df[8].str.split("-")
        df81 = df8.str[0]
        df82 = df8.str[1]
        df.insert(9, 8.5, df82)
        df[8] = df81
        df.columns = (
            ["aa_address"]
            + [f"aa_{x}" for x in range(16)]
            + ["aa_ascii"]
            + df.columns.to_list()[18:]
        )

    return df


def filter_memory_dataframe(
    df,
    fi,
    windbgexe,
    allowed_memstates="MEM_COMMIT",
    allowed_usages="Other|Heap|Stack|TEB",
):
    df.aa_RegionSize = (
        df.aa_RegionSize.str.replace("`", "")
        .ds_apply_ignore(pd.NA, lambda x: int(x, base=16))
        .astype("Int64")
    )

    dfdata = df.loc[
        (df.aa_State.str.contains(allowed_memstates, na=False, regex=True))
        & (df.aa_Usage.str.contains(allowed_usages, na=False, regex=True))
    ].reset_index(drop=True)
    lld = []
    for key, item in dfdata.iterrows():
        # break
        print(key, dfdata.shape[0], end="\r")
        s = "db " + item[1] + " " + item[2]
        data = get_windbg(
            command=s,
            procfile=fi,
            windbexe=windbgexe,
            timeout=ceil(item.aa_RegionSize / 1000),
        )
        dfa = convert_windbg2df(data, use_first_row_as_columns=False, dbcmd=True)
        if not dfa.empty:
            dfrep = pd.DataFrame(
                np.repeat(dfdata.loc[key:key], len(dfa), axis=1).reshape((-1, len(dfa)))
            ).T
            dfrep.columns = dfdata.columns.copy()
            dfa2 = pd.concat([dfa, dfrep], axis=1, ignore_index=False)
            lld.append(dfa2)

    return pd.concat(lld, ignore_index=True)


def get_tmpfile(suffix=".bin"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = filename.replace("/", os.sep).replace("\\", os.sep)
    tfp.close()
    return filename


def get_procdump(proc_dump_exe, pid):
    dumpfile = get_tmpfile(suffix=".dmp")
    erg = (
        ProcDump(executeable=proc_dump_exe)
        .o()
        .ma()
        .add_own_parameter_or_option(f"{pid}")
        .add_target_file_or_folder([dumpfile])
        .run()
    )
    return dumpfile


def get_handle_df(windbgexe, procfile):
    data = get_windbg(
        command="!handle",
        procfile=procfile,
        windbexe=windbgexe,
    )
    data1 = data[
        : [ini for ini, x in enumerate(data) if regex.search(rb"^\d+\s+Handles", x)][0]
    ]
    dfdata = convert_windbg2df(data1, use_first_row_as_columns=False, dbcmd=False)
    return pd.concat(
        [x.set_index(0).T for x in (np.split(dfdata, len(dfdata) // 2))],
        ignore_index=True,
    )


def get_lmu_df(windbgexe, procfile):
    data1 = get_windbg(
        command="lmu",
        procfile=procfile,
        windbexe=windbgexe,
    )
    data1 = [x for x in data1 if x.strip() and not x.startswith(b"Unloaded modules:")]
    dfdata = convert_windbg2df(data1, use_first_row_as_columns=True, dbcmd=False)
    return dfdata


def get_kv_df(windbgexe, procfile):
    data1 = get_windbg(
        command="kv",
        procfile=procfile,
        windbexe=windbgexe,
    )
    df2 = pd.DataFrame(
        [
            [y.strip().decode("utf-8", "ignore") for y in x.split(b" : ", maxsplit=2)]
            for x in data1
        ]
    )
    df3 = df2[0].str.split(r"\s+", n=1)
    df4 = pd.concat([df3.str[0], df3.str[1], df2[df2.columns[1:]]], axis=1)
    df4.columns = df4.iloc[0].copy()
    df4 = df4.drop(0).reset_index(drop=True)
    return df4


def get_df_from_mem_region(
    windbgexe,
    procfile,
    start_address="00007ff6`b6250000",
    end_address="00007ff6`b635d000",
):
    data1 = get_windbg(
        command=f"db {start_address} {end_address}",
        procfile=procfile,
        windbexe=windbgexe,
    )
    data1[-1] = (data1[-1] + 84 * b" ")[:84]
    data1a = np.char.array(data1).view("S1").reshape((-1, 84))
    v00_08 = data1a[..., 0:8].view(f"S{8 - 0}").ravel()
    v09_17 = data1a[..., 9:17].view(f"S{17 - 9}").ravel()

    v19 = data1a[..., 19:20].view(f"S1").ravel()
    v20 = data1a[..., 20:21].view(f"S1").ravel()
    v22 = data1a[..., 22:23].view(f"S1").ravel()
    v23 = data1a[..., 23:24].view(f"S1").ravel()
    v25 = data1a[..., 25:26].view(f"S1").ravel()
    v26 = data1a[..., 26:27].view(f"S1").ravel()
    v28 = data1a[..., 28:29].view(f"S1").ravel()
    v29 = data1a[..., 29:30].view(f"S1").ravel()
    v31 = data1a[..., 31:32].view(f"S1").ravel()
    v32 = data1a[..., 32:33].view(f"S1").ravel()
    v34 = data1a[..., 34:35].view(f"S1").ravel()
    v35 = data1a[..., 35:36].view(f"S1").ravel()
    v37 = data1a[..., 37:38].view(f"S1").ravel()
    v38 = data1a[..., 38:39].view(f"S1").ravel()
    v40 = data1a[..., 40:41].view(f"S1").ravel()
    v41 = data1a[..., 41:42].view(f"S1").ravel()
    v43 = data1a[..., 43:44].view(f"S1").ravel()
    v44 = data1a[..., 44:45].view(f"S1").ravel()
    v46 = data1a[..., 46:47].view(f"S1").ravel()
    v47 = data1a[..., 47:48].view(f"S1").ravel()
    v49 = data1a[..., 49:50].view(f"S1").ravel()
    v50 = data1a[..., 50:51].view(f"S1").ravel()
    v52 = data1a[..., 52:53].view(f"S1").ravel()
    v53 = data1a[..., 53:54].view(f"S1").ravel()
    v55 = data1a[..., 55:56].view(f"S1").ravel()
    v56 = data1a[..., 56:57].view(f"S1").ravel()
    v58 = data1a[..., 58:59].view(f"S1").ravel()
    v59 = data1a[..., 59:60].view(f"S1").ravel()
    v61 = data1a[..., 61:62].view(f"S1").ravel()
    v62 = data1a[..., 62:63].view(f"S1").ravel()
    v64 = data1a[..., 64:65].view(f"S1").ravel()
    v65 = data1a[..., 65:66].view(f"S1").ravel()
    v68_84 = data1a[..., 68:84].view(f"S{84 - 68}").ravel()

    alltransformcols = {
        "v19": v19,
        "v20": v20,
        "v22": v22,
        "v23": v23,
        "v25": v25,
        "v26": v26,
        "v28": v28,
        "v29": v29,
        "v31": v31,
        "v32": v32,
        "v34": v34,
        "v35": v35,
        "v37": v37,
        "v38": v38,
        "v40": v40,
        "v41": v41,
        "v43": v43,
        "v44": v44,
        "v46": v46,
        "v47": v47,
        "v49": v49,
        "v50": v50,
        "v52": v52,
        "v53": v53,
        "v55": v55,
        "v56": v56,
        "v58": v58,
        "v59": v59,
        "v61": v61,
        "v62": v62,
        "v64": v64,
        "v65": v65,
    }
    choicelist = np.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        dtype=np.uint8,
    )
    stan_val = np.uint8(0)

    splittetresultsdict = nested_dict()
    for k, v in alltransformcols.items():
        condlist = []
        for hexno, decno in zip(allhexnumbers, alldecnumbers):
            condlist.append(numexpr.evaluate(f"v == {repr(hexno)}"))

        allva = np.select(condlist, choicelist, stan_val)
        if k in ["v19", "v20"]:
            splittetresultsdict[21][k] = allva
        if k in ["v22", "v23"]:
            splittetresultsdict[24][k] = allva
        if k in ["v25", "v26"]:
            splittetresultsdict[27][k] = allva
        if k in ["v28", "v29"]:
            splittetresultsdict[30][k] = allva
        if k in ["v31", "v32"]:
            splittetresultsdict[33][k] = allva
        if k in ["v34", "v35"]:
            splittetresultsdict[36][k] = allva
        if k in ["v37", "v38"]:
            splittetresultsdict[39][k] = allva
        if k in ["v40", "v41"]:
            splittetresultsdict[42][k] = allva
        if k in ["v44", "v46"]:
            splittetresultsdict[45][k] = allva
        if k in ["v46", "v47"]:
            splittetresultsdict[48][k] = allva
        if k in ["v49", "v50"]:
            splittetresultsdict[51][k] = allva
        if k in ["v52", "v53"]:
            splittetresultsdict[54][k] = allva
        if k in ["v55", "v56"]:
            splittetresultsdict[57][k] = allva
        if k in ["v58", "v59"]:
            splittetresultsdict[60][k] = allva
        if k in ["v61", "v62"]:
            splittetresultsdict[63][k] = allva
        if k in ["v64", "v65"]:
            splittetresultsdict[66][k] = allva

    harra2 = v09_17.decode("utf-8")
    harra1 = v00_08.decode("utf-8")
    harrab = np.char.array(harra1) + np.char.array(harra2)
    harra3 = int_array(np.char.array(harrab).encode(), 16)
    alldfs = []
    goodcols = [
        "aa_address1_hex_block",
        "aa_address2_hex_block",
        "aa_address_int_block",
        "aa_address_sub",
        "aa_whole_string",
        "aa_Byte_int",
        "aa_2Bytes_int",
        "aa_4Bytes_int",
        "aa_8Bytes_int",
        "aa_4Bytes_float",
        "aa_8Bytes_float",
    ]
    for inino, indichar in enumerate(allindexchar):
        allfields = {}
        k1, k2 = list(splittetresultsdict[indichar].keys())
        uni0_0_00 = np.ascontiguousarray(splittetresultsdict[indichar][k1])
        uni0_1_00 = np.ascontiguousarray(splittetresultsdict[indichar][k2])
        uni1_0_04 = np.ascontiguousarray(
            np.left_shift(
                np.ascontiguousarray(uni0_0_00).astype(np.uint8),
                4,
            )
        )  # onebyte
        uni2_0_12 = np.left_shift(
            np.ascontiguousarray(uni0_0_00).astype(np.uint16),
            12,
        )  # 2 bytes
        uni2_1_08 = np.left_shift(
            np.ascontiguousarray(uni0_1_00).astype(np.uint16),
            8,
        )  # 2 bytes
        uni4_0_20 = np.left_shift(
            np.ascontiguousarray(uni0_0_00).astype(np.uint32),
            20,
        )  # 4 bytes
        uni4_0_28 = np.left_shift(
            np.ascontiguousarray(uni0_0_00).astype(np.uint32),
            28,
        )  # 4 bytes
        uni4_1_16 = np.left_shift(
            np.ascontiguousarray(uni0_1_00).astype(np.uint32),
            16,
        )  # 4 bytes
        uni4_1_24 = np.left_shift(
            np.ascontiguousarray(uni0_1_00).astype(np.uint32),
            24,
        )  # 4 bytes
        uni8_0_36 = np.left_shift(
            np.ascontiguousarray(uni0_0_00).astype(np.uint64),
            36,
        )  # 8 bytes
        uni8_0_44 = np.left_shift(
            np.ascontiguousarray(uni0_0_00).astype(np.uint64),
            44,
        )  # 8 bytes
        uni8_0_52 = np.left_shift(
            np.ascontiguousarray(uni0_0_00).astype(np.uint64),
            52,
        )  # 8 bytes
        uni8_0_58 = np.left_shift(
            np.ascontiguousarray(uni0_0_00).astype(np.uint64),
            58,
        )  # 8 bytes
        uni8_1_32 = np.left_shift(
            np.ascontiguousarray(uni0_1_00).astype(np.uint64),
            32,
        )  # 8 bytes
        uni8_1_40 = np.left_shift(
            np.ascontiguousarray(uni0_1_00).astype(np.uint64),
            40,
        )  # 8 bytes
        uni8_1_48 = np.left_shift(
            np.ascontiguousarray(uni0_1_00).astype(np.uint64),
            48,
        )  # 8 bytes
        uni8_1_56 = np.left_shift(
            np.ascontiguousarray(uni0_1_00).astype(np.uint64),
            56,
        )  # 8 bytes
        # 4 bytes
        allfields[f"bb_{indichar}_uni0_0_00"] = np.ascontiguousarray(uni0_0_00)
        allfields[f"bb_{indichar}_uni0_1_00"] = np.ascontiguousarray(uni0_1_00)
        allfields[f"bb_{indichar}_uni1_0_04"] = np.ascontiguousarray(uni1_0_04)
        allfields[f"bb_{indichar}_uni2_0_12"] = np.ascontiguousarray(uni2_0_12)
        allfields[f"bb_{indichar}_uni2_1_08"] = np.ascontiguousarray(uni2_1_08)
        allfields[f"bb_{indichar}_uni4_0_20"] = np.ascontiguousarray(uni4_0_20)
        allfields[f"bb_{indichar}_uni4_0_28"] = np.ascontiguousarray(uni4_0_28)
        allfields[f"bb_{indichar}_uni4_1_16"] = np.ascontiguousarray(uni4_1_16)
        allfields[f"bb_{indichar}_uni4_1_24"] = np.ascontiguousarray(uni4_1_24)
        allfields[f"bb_{indichar}_uni8_0_36"] = np.ascontiguousarray(uni8_0_36)
        allfields[f"bb_{indichar}_uni8_0_44"] = np.ascontiguousarray(uni8_0_44)
        allfields[f"bb_{indichar}_uni8_0_52"] = np.ascontiguousarray(uni8_0_52)
        allfields[f"bb_{indichar}_uni8_0_58"] = np.ascontiguousarray(uni8_0_58)
        allfields[f"bb_{indichar}_uni8_1_32"] = np.ascontiguousarray(uni8_1_32)
        allfields[f"bb_{indichar}_uni8_1_40"] = np.ascontiguousarray(uni8_1_40)
        allfields[f"bb_{indichar}_uni8_1_48"] = np.ascontiguousarray(uni8_1_48)
        allfields[f"bb_{indichar}_uni8_1_56"] = np.ascontiguousarray(uni8_1_56)
        df = pd.DataFrame.from_dict(allfields)
        df.columns = [x.split("_", maxsplit=2)[-1] for x in df.columns]
        df["aa_Byte_int"] = df.uni1_0_04.astype(np.uint8) + df.uni0_1_00.astype(
            np.uint8
        )
        df["aa_2Bytes_int"] = df.uni1_0_04 + df.uni0_1_00 + df.uni2_0_12 + df.uni2_1_08

        df["aa_4Bytes_int"] = (
            df.uni4_0_28
            + df.uni4_1_24
            + df.uni4_0_20
            + df.uni4_1_16
            + df["aa_2Bytes_int"].astype(np.uint64)
        )

        df["aa_8Bytes_int"] = (
            df.uni8_0_58
            + df.uni8_1_56
            + df.uni8_0_52
            + df.uni8_1_48
            + df.uni8_0_44
            + df.uni8_1_40
            + df.uni8_0_36
            + df.uni8_1_32
            + df["aa_4Bytes_int"].astype(np.uint64)
        )

        df.loc[:, "aa_4Bytes_float"] = np.ascontiguousarray(
            df["aa_4Bytes_int"].__array__().copy().view("b").view(np.float32)[::2]
        )
        df.loc[:, "aa_8Bytes_float"] = np.ascontiguousarray(
            df["aa_8Bytes_int"].__array__().copy().view("V8").view(np.float64)
        )

        df.loc[:, "aa_whole_string"] = v68_84
        df.insert(0, "aa_address_sub", harra3 + inino)

        df.insert(0, "aa_address_int_block", harra3)

        df.insert(0, "aa_address2_hex_block", harra2)

        df.insert(0, "aa_address1_hex_block", harra1)

        alldfs.append(df[goodcols].copy())
        gc.collect()

    df = (
        pd.concat(alldfs, ignore_index=True)
        .sort_values(by="aa_address_sub")
        .reset_index(drop=True)
    )
    df.loc[:, "aa_string"] = np.ascontiguousarray(df.aa_Byte_int.__array__().view("S1"))

    return df
