# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class Currency(str, enum.Enum):
    """
    ISO 4217 currency.  Its enumerants are ISO 4217 currencies except for
    some special currencies like ```XXX``.  Enumerants names are lowercase
    cureency code e.g. :attr:`Currency.eur`, :attr:`Currency.usd`.
    """

    AFN = "AFN"
    EUR = "EUR"
    ALL = "ALL"
    DZD = "DZD"
    USD = "USD"
    AOA = "AOA"
    XCD = "XCD"
    ARS = "ARS"
    AMD = "AMD"
    AWG = "AWG"
    AUD = "AUD"
    AZN = "AZN"
    BSD = "BSD"
    BHD = "BHD"
    BDT = "BDT"
    BBD = "BBD"
    BYN = "BYN"
    BZD = "BZD"
    XOF = "XOF"
    BMD = "BMD"
    INR = "INR"
    BTN = "BTN"
    BOB = "BOB"
    BOV = "BOV"
    BAM = "BAM"
    BWP = "BWP"
    NOK = "NOK"
    BRL = "BRL"
    BND = "BND"
    BGN = "BGN"
    BIF = "BIF"
    CVE = "CVE"
    KHR = "KHR"
    XAF = "XAF"
    CAD = "CAD"
    KYD = "KYD"
    CLP = "CLP"
    CLF = "CLF"
    CNY = "CNY"
    COP = "COP"
    COU = "COU"
    KMF = "KMF"
    CDF = "CDF"
    NZD = "NZD"
    CRC = "CRC"
    HRK = "HRK"
    CUP = "CUP"
    CUC = "CUC"
    ANG = "ANG"
    CZK = "CZK"
    DKK = "DKK"
    DJF = "DJF"
    DOP = "DOP"
    EGP = "EGP"
    SVC = "SVC"
    ERN = "ERN"
    SZL = "SZL"
    ETB = "ETB"
    FKP = "FKP"
    FJD = "FJD"
    XPF = "XPF"
    GMD = "GMD"
    GEL = "GEL"
    GHS = "GHS"
    GIP = "GIP"
    GTQ = "GTQ"
    GBP = "GBP"
    GNF = "GNF"
    GYD = "GYD"
    HTG = "HTG"
    HNL = "HNL"
    HKD = "HKD"
    HUF = "HUF"
    ISK = "ISK"
    IDR = "IDR"
    XDR = "XDR"
    IRR = "IRR"
    IQD = "IQD"
    ILS = "ILS"
    JMD = "JMD"
    JPY = "JPY"
    JOD = "JOD"
    KZT = "KZT"
    KES = "KES"
    KPW = "KPW"
    KRW = "KRW"
    KWD = "KWD"
    KGS = "KGS"
    LAK = "LAK"
    LBP = "LBP"
    LSL = "LSL"
    ZAR = "ZAR"
    LRD = "LRD"
    LYD = "LYD"
    CHF = "CHF"
    MOP = "MOP"
    MKD = "MKD"
    MGA = "MGA"
    MWK = "MWK"
    MYR = "MYR"
    MVR = "MVR"
    MRU = "MRU"
    MUR = "MUR"
    XUA = "XUA"
    MXN = "MXN"
    MXV = "MXV"
    MDL = "MDL"
    MNT = "MNT"
    MAD = "MAD"
    MZN = "MZN"
    MMK = "MMK"
    NAD = "NAD"
    NPR = "NPR"
    NIO = "NIO"
    NGN = "NGN"
    OMR = "OMR"
    PKR = "PKR"
    PAB = "PAB"
    PGK = "PGK"
    PYG = "PYG"
    PEN = "PEN"
    PHP = "PHP"
    PLN = "PLN"
    QAR = "QAR"
    RON = "RON"
    RUB = "RUB"
    RWF = "RWF"
    SHP = "SHP"
    WST = "WST"
    STN = "STN"
    SAR = "SAR"
    RSD = "RSD"
    SCR = "SCR"
    SLL = "SLL"
    SLE = "SLE"
    SGD = "SGD"
    XSU = "XSU"
    SBD = "SBD"
    SOS = "SOS"
    SSP = "SSP"
    LKR = "LKR"
    SDG = "SDG"
    SRD = "SRD"
    SEK = "SEK"
    CHE = "CHE"
    CHW = "CHW"
    SYP = "SYP"
    TWD = "TWD"
    TJS = "TJS"
    TZS = "TZS"
    THB = "THB"
    TOP = "TOP"
    TTD = "TTD"
    TND = "TND"
    TRY = "TRY"
    TMT = "TMT"
    UGX = "UGX"
    UAH = "UAH"
    AED = "AED"
    USN = "USN"
    UYU = "UYU"
    UYI = "UYI"
    UYW = "UYW"
    UZS = "UZS"
    VUV = "VUV"
    VES = "VES"
    VED = "VED"
    VND = "VND"
    YER = "YER"
    ZMW = "ZMW"
    ZWL = "ZWL"
    XBA = "XBA"
    XBB = "XBB"
    XBC = "XBC"
    XBD = "XBD"
    XTS = "XTS"
    XXX = "XXX"
    XAU = "XAU"
    XPD = "XPD"
    XPT = "XPT"
    XAG = "XAG"

    def visit(
        self,
        afn: typing.Callable[[], T_Result],
        eur: typing.Callable[[], T_Result],
        all: typing.Callable[[], T_Result],
        dzd: typing.Callable[[], T_Result],
        usd: typing.Callable[[], T_Result],
        aoa: typing.Callable[[], T_Result],
        xcd: typing.Callable[[], T_Result],
        ars: typing.Callable[[], T_Result],
        amd: typing.Callable[[], T_Result],
        awg: typing.Callable[[], T_Result],
        aud: typing.Callable[[], T_Result],
        azn: typing.Callable[[], T_Result],
        bsd: typing.Callable[[], T_Result],
        bhd: typing.Callable[[], T_Result],
        bdt: typing.Callable[[], T_Result],
        bbd: typing.Callable[[], T_Result],
        byn: typing.Callable[[], T_Result],
        bzd: typing.Callable[[], T_Result],
        xof: typing.Callable[[], T_Result],
        bmd: typing.Callable[[], T_Result],
        inr: typing.Callable[[], T_Result],
        btn: typing.Callable[[], T_Result],
        bob: typing.Callable[[], T_Result],
        bov: typing.Callable[[], T_Result],
        bam: typing.Callable[[], T_Result],
        bwp: typing.Callable[[], T_Result],
        nok: typing.Callable[[], T_Result],
        brl: typing.Callable[[], T_Result],
        bnd: typing.Callable[[], T_Result],
        bgn: typing.Callable[[], T_Result],
        bif: typing.Callable[[], T_Result],
        cve: typing.Callable[[], T_Result],
        khr: typing.Callable[[], T_Result],
        xaf: typing.Callable[[], T_Result],
        cad: typing.Callable[[], T_Result],
        kyd: typing.Callable[[], T_Result],
        clp: typing.Callable[[], T_Result],
        clf: typing.Callable[[], T_Result],
        cny: typing.Callable[[], T_Result],
        cop: typing.Callable[[], T_Result],
        cou: typing.Callable[[], T_Result],
        kmf: typing.Callable[[], T_Result],
        cdf: typing.Callable[[], T_Result],
        nzd: typing.Callable[[], T_Result],
        crc: typing.Callable[[], T_Result],
        hrk: typing.Callable[[], T_Result],
        cup: typing.Callable[[], T_Result],
        cuc: typing.Callable[[], T_Result],
        ang: typing.Callable[[], T_Result],
        czk: typing.Callable[[], T_Result],
        dkk: typing.Callable[[], T_Result],
        djf: typing.Callable[[], T_Result],
        dop: typing.Callable[[], T_Result],
        egp: typing.Callable[[], T_Result],
        svc: typing.Callable[[], T_Result],
        ern: typing.Callable[[], T_Result],
        szl: typing.Callable[[], T_Result],
        etb: typing.Callable[[], T_Result],
        fkp: typing.Callable[[], T_Result],
        fjd: typing.Callable[[], T_Result],
        xpf: typing.Callable[[], T_Result],
        gmd: typing.Callable[[], T_Result],
        gel: typing.Callable[[], T_Result],
        ghs: typing.Callable[[], T_Result],
        gip: typing.Callable[[], T_Result],
        gtq: typing.Callable[[], T_Result],
        gbp: typing.Callable[[], T_Result],
        gnf: typing.Callable[[], T_Result],
        gyd: typing.Callable[[], T_Result],
        htg: typing.Callable[[], T_Result],
        hnl: typing.Callable[[], T_Result],
        hkd: typing.Callable[[], T_Result],
        huf: typing.Callable[[], T_Result],
        isk: typing.Callable[[], T_Result],
        idr: typing.Callable[[], T_Result],
        xdr: typing.Callable[[], T_Result],
        irr: typing.Callable[[], T_Result],
        iqd: typing.Callable[[], T_Result],
        ils: typing.Callable[[], T_Result],
        jmd: typing.Callable[[], T_Result],
        jpy: typing.Callable[[], T_Result],
        jod: typing.Callable[[], T_Result],
        kzt: typing.Callable[[], T_Result],
        kes: typing.Callable[[], T_Result],
        kpw: typing.Callable[[], T_Result],
        krw: typing.Callable[[], T_Result],
        kwd: typing.Callable[[], T_Result],
        kgs: typing.Callable[[], T_Result],
        lak: typing.Callable[[], T_Result],
        lbp: typing.Callable[[], T_Result],
        lsl: typing.Callable[[], T_Result],
        zar: typing.Callable[[], T_Result],
        lrd: typing.Callable[[], T_Result],
        lyd: typing.Callable[[], T_Result],
        chf: typing.Callable[[], T_Result],
        mop: typing.Callable[[], T_Result],
        mkd: typing.Callable[[], T_Result],
        mga: typing.Callable[[], T_Result],
        mwk: typing.Callable[[], T_Result],
        myr: typing.Callable[[], T_Result],
        mvr: typing.Callable[[], T_Result],
        mru: typing.Callable[[], T_Result],
        mur: typing.Callable[[], T_Result],
        xua: typing.Callable[[], T_Result],
        mxn: typing.Callable[[], T_Result],
        mxv: typing.Callable[[], T_Result],
        mdl: typing.Callable[[], T_Result],
        mnt: typing.Callable[[], T_Result],
        mad: typing.Callable[[], T_Result],
        mzn: typing.Callable[[], T_Result],
        mmk: typing.Callable[[], T_Result],
        nad: typing.Callable[[], T_Result],
        npr: typing.Callable[[], T_Result],
        nio: typing.Callable[[], T_Result],
        ngn: typing.Callable[[], T_Result],
        omr: typing.Callable[[], T_Result],
        pkr: typing.Callable[[], T_Result],
        pab: typing.Callable[[], T_Result],
        pgk: typing.Callable[[], T_Result],
        pyg: typing.Callable[[], T_Result],
        pen: typing.Callable[[], T_Result],
        php: typing.Callable[[], T_Result],
        pln: typing.Callable[[], T_Result],
        qar: typing.Callable[[], T_Result],
        ron: typing.Callable[[], T_Result],
        rub: typing.Callable[[], T_Result],
        rwf: typing.Callable[[], T_Result],
        shp: typing.Callable[[], T_Result],
        wst: typing.Callable[[], T_Result],
        stn: typing.Callable[[], T_Result],
        sar: typing.Callable[[], T_Result],
        rsd: typing.Callable[[], T_Result],
        scr: typing.Callable[[], T_Result],
        sll: typing.Callable[[], T_Result],
        sle: typing.Callable[[], T_Result],
        sgd: typing.Callable[[], T_Result],
        xsu: typing.Callable[[], T_Result],
        sbd: typing.Callable[[], T_Result],
        sos: typing.Callable[[], T_Result],
        ssp: typing.Callable[[], T_Result],
        lkr: typing.Callable[[], T_Result],
        sdg: typing.Callable[[], T_Result],
        srd: typing.Callable[[], T_Result],
        sek: typing.Callable[[], T_Result],
        che: typing.Callable[[], T_Result],
        chw: typing.Callable[[], T_Result],
        syp: typing.Callable[[], T_Result],
        twd: typing.Callable[[], T_Result],
        tjs: typing.Callable[[], T_Result],
        tzs: typing.Callable[[], T_Result],
        thb: typing.Callable[[], T_Result],
        top: typing.Callable[[], T_Result],
        ttd: typing.Callable[[], T_Result],
        tnd: typing.Callable[[], T_Result],
        try_: typing.Callable[[], T_Result],
        tmt: typing.Callable[[], T_Result],
        ugx: typing.Callable[[], T_Result],
        uah: typing.Callable[[], T_Result],
        aed: typing.Callable[[], T_Result],
        usn: typing.Callable[[], T_Result],
        uyu: typing.Callable[[], T_Result],
        uyi: typing.Callable[[], T_Result],
        uyw: typing.Callable[[], T_Result],
        uzs: typing.Callable[[], T_Result],
        vuv: typing.Callable[[], T_Result],
        ves: typing.Callable[[], T_Result],
        ved: typing.Callable[[], T_Result],
        vnd: typing.Callable[[], T_Result],
        yer: typing.Callable[[], T_Result],
        zmw: typing.Callable[[], T_Result],
        zwl: typing.Callable[[], T_Result],
        xba: typing.Callable[[], T_Result],
        xbb: typing.Callable[[], T_Result],
        xbc: typing.Callable[[], T_Result],
        xbd: typing.Callable[[], T_Result],
        xts: typing.Callable[[], T_Result],
        xxx: typing.Callable[[], T_Result],
        xau: typing.Callable[[], T_Result],
        xpd: typing.Callable[[], T_Result],
        xpt: typing.Callable[[], T_Result],
        xag: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is Currency.AFN:
            return afn()
        if self is Currency.EUR:
            return eur()
        if self is Currency.ALL:
            return all()
        if self is Currency.DZD:
            return dzd()
        if self is Currency.USD:
            return usd()
        if self is Currency.AOA:
            return aoa()
        if self is Currency.XCD:
            return xcd()
        if self is Currency.ARS:
            return ars()
        if self is Currency.AMD:
            return amd()
        if self is Currency.AWG:
            return awg()
        if self is Currency.AUD:
            return aud()
        if self is Currency.AZN:
            return azn()
        if self is Currency.BSD:
            return bsd()
        if self is Currency.BHD:
            return bhd()
        if self is Currency.BDT:
            return bdt()
        if self is Currency.BBD:
            return bbd()
        if self is Currency.BYN:
            return byn()
        if self is Currency.BZD:
            return bzd()
        if self is Currency.XOF:
            return xof()
        if self is Currency.BMD:
            return bmd()
        if self is Currency.INR:
            return inr()
        if self is Currency.BTN:
            return btn()
        if self is Currency.BOB:
            return bob()
        if self is Currency.BOV:
            return bov()
        if self is Currency.BAM:
            return bam()
        if self is Currency.BWP:
            return bwp()
        if self is Currency.NOK:
            return nok()
        if self is Currency.BRL:
            return brl()
        if self is Currency.BND:
            return bnd()
        if self is Currency.BGN:
            return bgn()
        if self is Currency.BIF:
            return bif()
        if self is Currency.CVE:
            return cve()
        if self is Currency.KHR:
            return khr()
        if self is Currency.XAF:
            return xaf()
        if self is Currency.CAD:
            return cad()
        if self is Currency.KYD:
            return kyd()
        if self is Currency.CLP:
            return clp()
        if self is Currency.CLF:
            return clf()
        if self is Currency.CNY:
            return cny()
        if self is Currency.COP:
            return cop()
        if self is Currency.COU:
            return cou()
        if self is Currency.KMF:
            return kmf()
        if self is Currency.CDF:
            return cdf()
        if self is Currency.NZD:
            return nzd()
        if self is Currency.CRC:
            return crc()
        if self is Currency.HRK:
            return hrk()
        if self is Currency.CUP:
            return cup()
        if self is Currency.CUC:
            return cuc()
        if self is Currency.ANG:
            return ang()
        if self is Currency.CZK:
            return czk()
        if self is Currency.DKK:
            return dkk()
        if self is Currency.DJF:
            return djf()
        if self is Currency.DOP:
            return dop()
        if self is Currency.EGP:
            return egp()
        if self is Currency.SVC:
            return svc()
        if self is Currency.ERN:
            return ern()
        if self is Currency.SZL:
            return szl()
        if self is Currency.ETB:
            return etb()
        if self is Currency.FKP:
            return fkp()
        if self is Currency.FJD:
            return fjd()
        if self is Currency.XPF:
            return xpf()
        if self is Currency.GMD:
            return gmd()
        if self is Currency.GEL:
            return gel()
        if self is Currency.GHS:
            return ghs()
        if self is Currency.GIP:
            return gip()
        if self is Currency.GTQ:
            return gtq()
        if self is Currency.GBP:
            return gbp()
        if self is Currency.GNF:
            return gnf()
        if self is Currency.GYD:
            return gyd()
        if self is Currency.HTG:
            return htg()
        if self is Currency.HNL:
            return hnl()
        if self is Currency.HKD:
            return hkd()
        if self is Currency.HUF:
            return huf()
        if self is Currency.ISK:
            return isk()
        if self is Currency.IDR:
            return idr()
        if self is Currency.XDR:
            return xdr()
        if self is Currency.IRR:
            return irr()
        if self is Currency.IQD:
            return iqd()
        if self is Currency.ILS:
            return ils()
        if self is Currency.JMD:
            return jmd()
        if self is Currency.JPY:
            return jpy()
        if self is Currency.JOD:
            return jod()
        if self is Currency.KZT:
            return kzt()
        if self is Currency.KES:
            return kes()
        if self is Currency.KPW:
            return kpw()
        if self is Currency.KRW:
            return krw()
        if self is Currency.KWD:
            return kwd()
        if self is Currency.KGS:
            return kgs()
        if self is Currency.LAK:
            return lak()
        if self is Currency.LBP:
            return lbp()
        if self is Currency.LSL:
            return lsl()
        if self is Currency.ZAR:
            return zar()
        if self is Currency.LRD:
            return lrd()
        if self is Currency.LYD:
            return lyd()
        if self is Currency.CHF:
            return chf()
        if self is Currency.MOP:
            return mop()
        if self is Currency.MKD:
            return mkd()
        if self is Currency.MGA:
            return mga()
        if self is Currency.MWK:
            return mwk()
        if self is Currency.MYR:
            return myr()
        if self is Currency.MVR:
            return mvr()
        if self is Currency.MRU:
            return mru()
        if self is Currency.MUR:
            return mur()
        if self is Currency.XUA:
            return xua()
        if self is Currency.MXN:
            return mxn()
        if self is Currency.MXV:
            return mxv()
        if self is Currency.MDL:
            return mdl()
        if self is Currency.MNT:
            return mnt()
        if self is Currency.MAD:
            return mad()
        if self is Currency.MZN:
            return mzn()
        if self is Currency.MMK:
            return mmk()
        if self is Currency.NAD:
            return nad()
        if self is Currency.NPR:
            return npr()
        if self is Currency.NIO:
            return nio()
        if self is Currency.NGN:
            return ngn()
        if self is Currency.OMR:
            return omr()
        if self is Currency.PKR:
            return pkr()
        if self is Currency.PAB:
            return pab()
        if self is Currency.PGK:
            return pgk()
        if self is Currency.PYG:
            return pyg()
        if self is Currency.PEN:
            return pen()
        if self is Currency.PHP:
            return php()
        if self is Currency.PLN:
            return pln()
        if self is Currency.QAR:
            return qar()
        if self is Currency.RON:
            return ron()
        if self is Currency.RUB:
            return rub()
        if self is Currency.RWF:
            return rwf()
        if self is Currency.SHP:
            return shp()
        if self is Currency.WST:
            return wst()
        if self is Currency.STN:
            return stn()
        if self is Currency.SAR:
            return sar()
        if self is Currency.RSD:
            return rsd()
        if self is Currency.SCR:
            return scr()
        if self is Currency.SLL:
            return sll()
        if self is Currency.SLE:
            return sle()
        if self is Currency.SGD:
            return sgd()
        if self is Currency.XSU:
            return xsu()
        if self is Currency.SBD:
            return sbd()
        if self is Currency.SOS:
            return sos()
        if self is Currency.SSP:
            return ssp()
        if self is Currency.LKR:
            return lkr()
        if self is Currency.SDG:
            return sdg()
        if self is Currency.SRD:
            return srd()
        if self is Currency.SEK:
            return sek()
        if self is Currency.CHE:
            return che()
        if self is Currency.CHW:
            return chw()
        if self is Currency.SYP:
            return syp()
        if self is Currency.TWD:
            return twd()
        if self is Currency.TJS:
            return tjs()
        if self is Currency.TZS:
            return tzs()
        if self is Currency.THB:
            return thb()
        if self is Currency.TOP:
            return top()
        if self is Currency.TTD:
            return ttd()
        if self is Currency.TND:
            return tnd()
        if self is Currency.TRY:
            return try_()
        if self is Currency.TMT:
            return tmt()
        if self is Currency.UGX:
            return ugx()
        if self is Currency.UAH:
            return uah()
        if self is Currency.AED:
            return aed()
        if self is Currency.USN:
            return usn()
        if self is Currency.UYU:
            return uyu()
        if self is Currency.UYI:
            return uyi()
        if self is Currency.UYW:
            return uyw()
        if self is Currency.UZS:
            return uzs()
        if self is Currency.VUV:
            return vuv()
        if self is Currency.VES:
            return ves()
        if self is Currency.VED:
            return ved()
        if self is Currency.VND:
            return vnd()
        if self is Currency.YER:
            return yer()
        if self is Currency.ZMW:
            return zmw()
        if self is Currency.ZWL:
            return zwl()
        if self is Currency.XBA:
            return xba()
        if self is Currency.XBB:
            return xbb()
        if self is Currency.XBC:
            return xbc()
        if self is Currency.XBD:
            return xbd()
        if self is Currency.XTS:
            return xts()
        if self is Currency.XXX:
            return xxx()
        if self is Currency.XAU:
            return xau()
        if self is Currency.XPD:
            return xpd()
        if self is Currency.XPT:
            return xpt()
        if self is Currency.XAG:
            return xag()
