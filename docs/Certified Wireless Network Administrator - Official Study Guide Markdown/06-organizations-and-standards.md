# Chapter 6 - Organizations & Standards

_PDF pages 174-195_

##### Wireless LAN Organizations and Standards

**CWNA Exam Objectives Covered:**

- Identify, apply, and comprehend the differences between the
following wireless LAN standards:

 - 802.11

 - 802.11b

 - 802.11a

 - 802.11g

 - Bluetooth

 - Infrared

 - HomeRF

- Understand the roles of the following organizations in providing
direction and accountability within the wireless LAN industry:

 - FCC

 - IEEE

 - WECA

 - WLANA

 - IrDA

 - ETSI

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

**CHAPTER**
# 5 6

**In This Chapter**

FCC

IEEE

Wireless LAN Organizations

Competing Technologies

--- end of page=173 ---

Chapter 6 – Wireless LAN Organizations and Standards **146**

Most computer-related hardware and technologies are based on some standards, and
wireless LANs are no exception. There are organizations that define and support the
standards that allow hardware from different manufacturers to function together
seamlessly. In this chapter we will discuss the FCC’s role in defining and enforcing the
laws governing wireless communication and the IEEE’s role in creating standards that
allow wireless devices to work together. We will also cover the different frequency
bands on which wireless LANs operate, and examine the 802.11 family of standards. We
will discuss some of the major organizations in the wireless LAN marketplace as well as
the roles they fill in the industry. Finally, we will cover some of the emerging
technologies and standards and discuss their impact on the wireless LAN industry.

By understanding the laws and the standards that govern and guide wireless LAN
technology, you will be able to ensure that any wireless system you implement will be
interoperable and comply with the law. Furthermore, familiarity with these statutes and
standards, as well as the organizations that create them, will greatly enhance your ability
to research and find the latest information about wireless LANs.

##### Federal Communications Commission

The Federal Communications Commission (FCC) is an independent United States
government agency, directly responsible to Congress. The FCC was established by the
Communications Act of 1934 and is charged with regulating interstate and international
communications by radio, television, wire, satellite, and cable. The FCC's jurisdiction
covers not only the 50 states and the District of Columbia, but also all U.S. possessions
such as Puerto Rico, Guam, and The Virgin Islands.

The FCC makes the laws within which wireless LAN devices must operate. The FCC
mandates where on the radio frequency spectrum wireless LANs can operate and at what
power, using which transmission technologies, and how and where various pieces of
wireless LAN hardware may be used.

![](images/06-organizations-and-standards.pdf-174-0.png)

**ISM and UNII Bands**

The FCC establishes rules limiting which frequencies wireless LANs can use and the
output power on each of those frequency bands. The FCC has specified that wireless
LANs can use the Industrial, Scientific, and Medical (ISM) bands, which are license free.
The ISM bands are located starting at 902 MHz, 2.4 GHz, and 5.8 GHz and vary in width
from about 26 MHz to 150 MHz.

In addition to the ISM bands, the FCC specifies three Unlicensed National Information
Infrastructure (UNII) bands. Each one of these UNII bands is in the 5 GHz range and is
100 MHz wide. Figure 6.1 illustrates the ISM and UNII bands available.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=174 ---

**147** Chapter 6 – Wireless LAN Organizations and Standards

**FIGURE 6.1** ISM and UNII Spectra

|ISM|Col2|
|---|---|
|2.4000-2.4835 GHz<br>||
|2.4000-2.5000 GHz|2.4000-2.5000 GHz|

|Col1|5 NII EE|
|---|---|
||<br>5|
|||

|ISM 250 5.500 5.750 6.0|Col2|Col3|
|---|---|---|
|5.725-5.875 GHz|5.725-5.875 GHz|5.725-5.875 GHz|
||||

|5.15 - 5.25 - 5.725 -<br>IEEE: 2.4000-2.4835 GHz 5.25 GHz 5.35 GHz 5.825 G<br>FCC: 2.4000-2.5000 GHz<br>2.400 2.425 2.450 2.475 2.500 5.000 5.250 5.500 5.750 6.000<br>GHz GHz<br>ISM<br>FCC: 5.725-5.875 GHz<br>ISM<br>: 902-928MHz<br>5.725 5.775 5.825 5.875<br>GHz<br>00 910 920 930<br>Hz<br>Maritime, Radio Astronomy F Research, Navigation Nav, Nav. Nav.<br>M Astronomy|Col2|Col3|
|---|---|---|
|Maritime, Radio Astronomy|F<br>M|Research, Navigation|

10 100 1 10
MHz MHz GHz GHz

**Advantages and Disadvantages of License-Free Bands**

When implementing any wireless system on a license-free band, there is no requirement
to petition the FCC for bandwidth and power needs. Limits on the power of transmission
exist, but there is no procedure for receiving permission to transmit at such power.
Furthermore, there are no licensing requirements and, thus, no cost associated with
licensing. The license-free nature of the ISM and UNII bands is very important because
it allows entities like small businesses and households to implement wireless systems and
fosters the growth of the wireless LAN market.

Such freedom from licensing carries with it a major disadvantage to license-free band
users. The same license-free band you use (or intend to use) is also license-free to others.
Suppose you install a wireless LAN segment on your home network. If your neighbor
also installs a wireless LAN segment in his home, his system may interfere with yours,
and vise versa. Furthermore, if he uses a higher-power system, his wireless LAN may
disable yours by “whiting out” your wireless traffic. The two competing systems don’t
necessarily have to be on the same channel, or even be the same spread spectrum
technology.

**Industrial Scientific Medical (ISM) Bands**

There are three license-free ISM bands the FCC has specified that wireless LANs may
use. They are the 900 MHz, 2.4 GHz, and 5.8 GHz bands.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=175 ---

Chapter 6 – Wireless LAN Organizations and Standards **148**

**900 MHz ISM Band**

The 900 MHz ISM band is defined as the range of frequencies from 902 MHz to 928
MHz. This band may be additionally (and correctly) defined as 915 MHz ± 13 MHz.
Though the 900 MHz ISM band was once used by wireless LANs, it has been largely
abandoned in favor of the higher frequency bands, which have wider bandwidths and
allow more throughput. Some of the wireless devices that still use the 900 MHz band are
wireless home phones and wireless camera systems. Organizations that use 900 MHz
wireless LANs find out the hard way that obsolete equipment is expensive to replace
should any piece of their hardware malfunctions. A single 900 MHz radio card may cost
as much as $800 and might only be able to transmit at speeds up to 1 Mbps. In
comparison, an 802.11b compliant wireless card will support speeds up to 11 Mbps and
sell for roughly $100. Finding support or replacements for these older 900 MHz units is
almost impossible.

**2.4 GHz ISM Band**

This band is used by all 802.11, 802.11b, and 802.11g-compliant devices and is by far the
most populated space of the three bands presented in this chapter. The 2.4 GHz ISM
band is bound by 2.4000 GHz and 2.5000 GHz (2.4500 GHz ± 50 MHz), as defined by
the FCC. Of the 100 MHz between 2.4000 and 2.5000 GHz, only the frequencies 2.4000

      - 2.4835 GHz are actually used by wireless LAN devices. The principal reason for this
limitation is that the FCC has specified power output only for this range of frequencies
within the 2.4 GHz ISM band.

**5.8 GHz ISM Band**

This band is also frequently called the 5 GHz ISM Band. The 5.8 GHz ISM is bound by
5.725 GHz and 5.875 GHz, which yields a 150 MHz bandwidth. This band of
frequencies is _not_ specified for use by wireless LAN devices, so it tends to present some
confusion. The 5.8 GHz ISM band overlaps part of another license-free band, the Upper
UNII band, causing the 5.8 GHz ISM band to be confused with the 5 GHz Upper UNII
band, which _is_ used with wireless LANs.

**Unlicensed National Information Infrastructure (UNII) Bands**

The 5 GHz UNII bands are made up of three separate 100 MHz-wide bands, which are
used by 802.11a-compliant devices. The three bands are known as the lower, middle, and
upper bands. Within each of these three bands, there are four non-overlapping DSSS
channels, each separated by 5 MHz. The FCC mandates that the lower band be used
indoors, the middle band be used indoors or outdoors, and the upper band be allocated for
outdoor use. Since access points are mostly mounted indoors, the 5 GHz UNII bands
would allow for 8 non-overlapping access points indoors using both the lower and middle
UNII bands.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=176 ---

**149** Chapter 6 – Wireless LAN Organizations and Standards

**Lower Band**

The lower band is bound by 5.15 GHz and 5.25 GHz and is specified by the FCC to have
a maximum output power of 50 mW. When implementing 802.11a compliant devices,
the IEEE has specified 40 mW (80%) as the maximum output power for 802.11acompliant radios, reserving the lower band for indoor operation only.

![](images/06-organizations-and-standards.pdf-177-0.png)

**Middle Band**

The middle UNII band is bound by 5.25 GHz and 5.35 GHz and is specified at 250 mW
of output power by the FCC. The power output specified by IEEE for the middle UNII
band is 200 mW. This power limit allows operation of devices either indoors or outdoors
and is commonly used for short outdoor hops between closely spaced buildings. In the
case of a home installation, such a configuration might include an RF link between the
house and the garage, or the house and a neighbor’s house. Due to reasonable power
output and flexible indoor/outdoor use restrictions, products manufactured to work in the
middle UNII band could enjoy wide acceptance in the future.

**Upper Band**

The upper UNII band is reserved for outdoor links and is limited by the FCC to 1 Watt
(1000 mW) of output power. This band occupies the range of frequencies between 5.725
GHz and 5.825 GHz, and is often confused with the 5.8 GHz ISM band. The IEEE
specifies the maximum output power for this band as 800 mW, which is plenty of power
for almost any outdoor implementation, except for large campuses or long-distance RF
links.

**Power Output Rules**

The FCC enforces certain rules regarding the power radiated by the antenna element,
depending on whether the implementation is a point-to-multipoint or a point-to-point
implementation. The term used for the power radiated by the antenna is _Equivalent_
_Isotropically Radiated Power_ (EIRP).

**Point-to-Multipoint (PtMP)**

PtMP links have a central point of connection and two or more non-central connection
points. PtMP links are typically configured in a hub-n-spoke topology. The central
connection point may or may not have an omnidirectional antenna (an omnidirectional
antenna produces a 360 degree horizontal beam). It is important to note that when an
omnidirectional antenna is used, the FCC automatically considers the link a PtMP link.
Regarding the setup of a PtMP link, the FCC limits the EIRP to 4 Watts in both the 2.4

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=177 ---

Chapter 6 – Wireless LAN Organizations and Standards **150**

GHz ISM band and upper 5 GHz UNII band. Furthermore, the power limit set for the
intentional radiator (the device transmitting the RF signal) in each of these bands is 1
Watt. If the transmitting wireless LAN devices are adjustable with respect to their output
power, then the system can be customized to the needs of the user.

Suppose a radio transmitting at 1 Watt (+30 dBm) is connected directly to a 12 dBi
omnidirectional antenna. The total output power at the antenna is about 16 Watts, which
is well above the 4 Watt limit. The FCC stipulates that _for each 3 dBi above the_
_antenna's initial 6 dBi of gain, the power at the intentional radiator must be reduced by 3_
_dB below the initial +30 dBm_ . For our example, since the antenna gain is 12 dBi, the
power at the intentional radiator must be reduced by 6 dB. This reduction will result in
an intentional radiator power of +24 dBm (30 dBm – 6 dB), or 250 mW and an EIRP of
36 dBm (24 dBm + 12 dBi), or 4 Watts. Clearly this rule can become confusing, but the
end result must be that the power at the intentional radiator never be more than 1 Watt
(see Figure 6.2), and the EIRP must never be above 4 Watts for a PtMP connection.

**FIGURE 6.2** Point-to-Multipoint Power Compensation Table

|Power at Antenna<br>(dBm)|Antenna Gain<br>(dBi)|EIRP<br>(dBm)|EIRP<br>(watts)|
|---|---|---|---|
|30|6|36|4|
|27|9|36|4|
|24|12|36|4|
|21|15|36|4|
|18|18|36|4|
|15|21|36|4|
|12|24|36|4|

![](images/06-organizations-and-standards.pdf-178-0.png)

When using an omnidirectional antenna, the rules for point-to-multipoint links must be
followed, regardless of whether the actual implementation is point-to-point or point-tomultipoint.

**Point-to-Point (PtP)**

PtP links include a single directional transmitting antenna and a single directional
receiving antenna. These connections will typically include building-to-building or
similar links and must abide by special rules. When installing a PtP link, the 4 Watt
power limit all but disappears in favor of a sliding power limit. Regarding a PtP link, the
FCC mandates that _for every 3 dBi above the initial 6 dBi of antenna gain, the power at_
_the intentional radiator must be reduced by 1 dB below the initial +30 dBm_ .

Consider our previous example, using the same values: 1 Watt (+30 dBm) at the
intentional radiator and a 12 dBi antenna (in this case the antenna will be a directional
antenna). The total output power is still 16 Watts. In this example, since the antenna

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=178 ---

**151** Chapter 6 – Wireless LAN Organizations and Standards

gain is 12 dBi, the power at the intentional radiator must be reduced by 2 dB, as opposed
to a 6 dB reduction in the previous example. This reduction will result in an intentional
radiator power of 28 dBm (30 dBm – 2 dB), or about 630 mW and an EIRP of 40 dBm
(28 dBm + 12 dBi), or 10 Watts. In the case of PtP links, the power at the intentional
radiator is still limited to 1 Watt, but the limit of the EIRP _increases_ with the gain of the
antenna (Figure 6.3). It is very important to clearly distinguish between the rules that
govern PtP and PtMP wireless links.

**FIGURE 6.3** Point-to-Point Power Compensation Table

|Power at Antenna<br>(dBm)|Max Antenna Gain<br>(dBi)|EIRP<br>(dBm)|EIRP<br>(watts)|
|---|---|---|---|
|30|6|36|4|
|29|9|38|6.3|
|28|12|40|10|
|27|15|42|16|
|26|18|44|25|
|25|21|46|39.8|
|24|24|48|63|
|23|27|50|100|
|22|30|52|158|

![](images/06-organizations-and-standards.pdf-179-0.png)

##### Institute of Electrical and Electronics Engineers

The Institute of Electrical and Electronics Engineers ( _IEEE_ ) is the key standards maker
for most things related to information technology in the United States. The IEEE creates
its standards within the laws created by the FCC. The IEEE specifies many technology
standards such as Public Key Cryptography (IEEE 1363), FireWire (IEEE 1394),
Ethernet (IEEE 802.3), and Wireless LANs (IEEE 802.11).

![](images/06-organizations-and-standards.pdf-179-1.png)

It is part of the mission of the IEEE to develop standards for wireless LAN operation
within the framework of the FCC rules and regulations. Following are the four main
IEEE standards for wireless LANs that are either in use or in draft form:

 - 802.11

 - 802.11b

 - 802.11a

 - 802.11g

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=179 ---

Chapter 6 – Wireless LAN Organizations and Standards **152**

**IEEE 802.11**

The 802.11 standard was the first standard describing the operation of wireless LANs.
This standard contained all of the available transmission technologies including Direct
Sequence Spread Spectrum (DSSS), Frequency Hopping Spread Spectrum (FHSS), and
infrared.

![](images/06-organizations-and-standards.pdf-180-0.png)

The IEEE 802.11 standard describes DSSS systems that operate at 1 Mbps and 2 Mbps
only. If a DSSS system operates at other data rates as well, such as 1 Mbps, 2 Mbps, and
11 Mbps, then it can still be an 802.11-compliant system. If, however, the system is
operating at any rate other than 1 or 2 Mbps, then, even though the system is 802.11compliant because of its ability to work at 1 & 2 Mbps, it is not operating in an 802.11compliant mode and cannot be expected to communicate with other 802.11-compliant
devices.

IEEE 802.11 is one of two standards that describe the operation of frequency hopping
wireless LAN systems. If a wireless LAN administrator encounters a frequency hopping
system, then it is likely to be either an 802.11-compliant or OpenAir compliant system
(discussed below). The 802.11 standard describes use of FHSS systems at 1 and 2 Mbps.
There are many FHSS systems on the market that extend this functionality by offering
proprietary modes that operate at 3-10 Mbps, but just as with DSSS, if the system is
operating at speeds other than 1 & 2 Mbps, it cannot be expected to automatically
communicate with other 802.11-compliant devices.

802.11 compliant products operate strictly in the 2.4 GHz ISM band between 2.4000 and
2.4835 GHz. Infrared, also covered by 802.11, is light-based technology and does not
fall into the 2.4 GHz ISM band.

**IEEE 802.11b**

Though the 802.11 standard was successful in allowing DSSS as well as FHSS systems
to interoperate, the technology has outgrown the standard. Soon after the approval and
implementation of 802.11, DSSS wireless LANs were exchanging data at up to 11 Mbps.
But, without a standard to guide the operation of such devices, there came to be problems
with interoperability and implementation. The manufacturers ironed out most of the
implementation problems, so the job of IEEE was relatively easy: create a standard that
complied with the general operation of wireless LANs then on the market. It is not
uncommon for the standards to follow the technology in this way, particularly when the
technology evolves quickly.

IEEE 802.11b, referred to as "High-Rate" and Wi-Fi™, specifies direct sequencing
(DSSS) systems that operate at 1, 2, 5.5 and 11 Mbps. The 802.11b standard does _not_
describe any FHSS systems, and 802.11b-compliant devices are also 802.11-compliant
by default, meaning they are backward compatible and support both 2 and 1 Mbps data
rates. Backward compatibility is very important because it allows a wireless LAN to be

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=180 ---

**153** Chapter 6 – Wireless LAN Organizations and Standards

upgraded without the cost of replacing the core hardware. This low-cost feature, together
with the high data rate, has made the 802.11b-compliant hardware very popular.

The high data rate of 802.11b-compliant devices is the result of using a different coding
technique. Though the system is still a direct sequencing system, the way the chips are
coded (CCK rather than Barker Code) along with the way the information is modulated
(QPSK at 2, 5.5, & 11 Mbps and BPSK at 1 Mbps) allows for a greater amount of data to
be transferred in the same time frame. 802.11b compliant products operate only in the
2.4 GHz ISM band between 2.4000 and 2.4835 GHz. Modulation and coding are further
discussed in Chapter 8 (MAC & Physical Layers).

**IEEE 802.11a**

The IEEE 802.11a standard describes wireless LAN device operation in the 5 GHz UNII
bands. Operation in the UNII bands automatically makes 802.11a devices incompatible
with all other devices complying with the other 802.11 series of standards. The reason
for this incompatibility is simple: systems using 5 GHz frequencies will not communicate
with systems using 2.4 GHz frequencies.

Using the UNII bands, most devices are able to achieve data rates of 6, 9, 12, 18, 24, 36,
48, and 54 Mbps. Some of the devices employing the UNII bands have achieved data
rates of 108 Mbps by using proprietary technology, such as _rate doubling_ . The highest
rates of some of these devices are the result of newer technologies not specified by the
802.11a standard. IEEE 802.11a specifies data rates of only 6, 12, and 24 Mbps. A
wireless LAN device must support at least these data rates in the UNII bands in order to
be 802.11a-compliant. The maximum data rate specified by the 802.11a standard is 54
Mbps.

**IEEE 802.11g**

802.11g provides the same maximum speed of 802.11a, coupled with backwards
compatibility for 802.11b devices. This backwards compatibility will make upgrading
wireless LANs simple and inexpensive. Since 802.11g technology is new, 802.11g
devices are not yet available as of this writing.

IEEE 802.11g specifies operation in the 2.4 GHz ISM band. To achieve the higher data
rates found in 802.11a, 802.11g compliant devices utilize Orthogonal Frequency Division
Multiplexing (OFDM) modulation technology. These devices can automatically switch
to QPSK modulation in order to communicate with the slower 802.11b- and 802.11compatable devices. With all of the apparent advantages, 802.11g’s use of the crowded
2.4 GHz band could prove to be a disadvantage.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

![](images/06-organizations-and-standards.pdf-181-0.png)

--- end of page=181 ---

Chapter 6 – Wireless LAN Organizations and Standards **154**

##### Major Organizations

Whereas the FCC and the IEEE are responsible for defining the laws and standards as
they apply to wireless LANs in the United States, there are several other organizations,
both in the U.S. and in other countries, that contribute to growth and education in the
wireless LAN marketplace. In this section, we will look at three of these organizations:

      - Wireless Ethernet Compatibility Alliance (WECA)

      - European Telecommunications Standards Institute (ETSI)

      - Wireless LAN Association (WLANA)

**Wireless Ethernet Compatibility Alliance**

The Wireless Ethernet Compatibility Alliance ( _WECA_ ) promotes and tests for wireless
LAN interoperability of 802.11b devices and 802.11a devices. WECA’s mission is _to_
_certify interoperability of Wi-Fi™ (IEEE 802.11) products and to promote Wi-Fi as the_
_global wireless LAN standard across all market segments_ . As an administrator, you must
resolve conflicts among wireless LAN devices that result from interference,
incompatibility, or other problems.

When a product meets the interoperability requirements as described in WECA's test
matrix, WECA grants the product a certification of interoperability, which allows the
vendor to use the Wi-Fi logo on advertising and packaging for the certified product. The
Wi-Fi seal of approval assures the end user of interoperability with other wireless LAN
devices that also bear the Wi-Fi logo.

Among WECA's list of interoperability checks is the use of 40-bit WEP keys. Note that
40- and 64-bit keys are the same thing. A 40-bit "secret" key is concatenated with a 24bit Initialization Vector (IV) to reach the 64-bits. In the same manner, 104- and 128-bit
keys are the same. WECA does not specify interoperability of 128-bit keys; hence, no
compatibility is to be expected between vendors displaying the Wi-Fi seal when using
128-bit WEP keys. Nevertheless, many 128-bit systems from different vendors are
interoperable.

There are many other factors besides use of 40-bit WEP keys that are required to meet
WECA's Wi-Fi criteria. These factors include support of fragmentation, PSP mode,
ESSIDs, SSID probe requests, and others. Some of these topics will be discussed in later
chapters.

![](images/06-organizations-and-standards.pdf-182-0.png)

**European Telecommunications Standards Institute**

The European Telecommunications Standards Institute (ETSI) is chartered with
producing communications standards for Europe in the same way that the IEEE is for the

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=182 ---

**155** Chapter 6 – Wireless LAN Organizations and Standards

United States. The standards ETSI has established, HiPerLAN/2 for example, directly
compete against standards created by the IEEE such as 802.11a. There has been much
discussion about IEEE and ETSI unifying on certain wireless technologies, but nothing
has materialized as of this writing. This effort is referred to as the "5UP" initiative for "5
GHz Unified Protocol." The IEEE's attempt at interoperability with ETSI's HiperLAN/2
standard is the new forthcoming 802.11h standard.

ETSI's original HiPerLAN standard for wireless, dubbed HiperLAN/1, supported rates of
up to 24 Mbps using DSSS technology with a range of approximately 150 feet.
HiperLAN/1 used the lower and middle UNII bands, as do HiperLAN/2, 802.11a, and the
new 802.11h standard. The new HiperLAN/2 standard supports rates of up to 54 Mbps
and uses all three of the UNII bands.

ETSI's HiperLAN/2 standard has interchangeable convergence layers, support for QoS,
and supports DES and 3DES encryption. The supported convergence layers are ATM,
Ethernet, PPP, FireWire, and 3G. Supported QoS awareness includes 802.1p, RSVP, and
DiffServ-FC.

**Wireless LAN Association**

The Wireless LAN Association's mission is to educate and raise consumer awareness
regarding the use and availability of wireless LANs and to promote the wireless LAN
industry in general. The Wireless LAN Association ( _WLANA_ ) is an educational resource
for those seeking to learn more about wireless LANs. WLANA can also help if you are
looking for a specific wireless LAN product or service.

WLANA has many partners within the industry that contribute content to the WLANA
directory of information. It is this directory, along with the many white papers and case
studies that WLANA provides, that offer you valuable information for making your own
decisions about wireless LAN implementation.

![](images/06-organizations-and-standards.pdf-183-0.png)

##### Competing Technologies

There are several technologies that compete with the 802.11 family of standards. As
business needs change, and technologies improve, there will continue to be new standards
created to support the marketplace as well as new inventions that drive enterprise
spending. Other wireless LAN technologies and standards that are in use today include:

      - HomeRF

      - Bluetooth

      - Infrared

      - OpenAir

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=183 ---

Chapter 6 – Wireless LAN Organizations and Standards **156**

**HomeRF**

HomeRF operates in the 2.4 GHz band and uses frequency hopping technology.
HomeRF devices hop at about 50 hops per seconds—about 5 to 20 times faster than most
802.11-compliant FHSS devices. The new version of HomeRF, HomeRF 2.0 uses the
new “wide band” frequency hopping rules approved by the FCC, and is the first to do so.
Recall that these rules, implemented after 08/31/00, include:

     - Maximum of 5 MHz wide carrier frequencies

     - Minimum of 15 hops in a sequence

     - Maximum of 125 mW of output power

Because HomeRF allows an increase over the former 1 MHz wide carrier frequencies,
and flexibility in implementing less than the previously required 75 hops, one might think
that wide band frequency hopping would be quite popular among corporations and
vendors alike. This, however, is not the case. As advantageous as the resulting 10 Mbps
data rate is, it does not overshadow the disadvantage of 125 mW of output power, which
limits use of wide band frequency hopping devices to an approximate range of 150 feet.
This outcome limits the use of wideband frequency hopping devices primarily to SOHO
environments.

HomeRF units use the SWAP protocol, which is a combination of CSMA (used in local
area networks) and TDMA (used in cellular phones) protocols. SWAP is a hybrid of the
802.11 and DECT standards and was developed by the HomeRF working group.
HomeRF devices are the only devices currently on the market that follow the wideband
frequency hopping rules. HomeRF devices are considered more secure than 802.11
products using WEP because of the 32-bit initialization vector (IV) HomeRF uses (in
contrast to 802.11's 24-bit IV). Additionally, HomeRF has specified how the IV is to be
chosen during encryption, whereas 802.11 does not, leaving 802.11 open for attack due to
weak implementations.

**Bluetooth**

Bluetooth is another frequency hopping technology that operates in the 2.4 GHz ISM
band. The hop rate of Bluetooth devices is about 1600 hops per second (about 625µs
dwell time), so it has considerably more overhead than 802.11-compliant frequency
hopping systems. The high hop rate also gives the technology greater resistance to
spurious narrow band noise. Bluetooth systems are not designed for high throughput, but
rather for simple use, low power, and short range (WPANs). The new IEEE 802.15 draft
for WPANs includes specifications for Bluetooth.

A major disadvantage of using Bluetooth technology is that it tends to completely disrupt
other 2.4 GHz networks. The high hop rate of Bluetooth over the entire usable 2.4 GHz
band makes the Bluetooth signal appear to all other systems as _all-band noise_, or _all-_
_band interference_ . Bluetooth also affects other FHSS systems. All-band interference, as
the name implies, disrupts the signal over its entire range of useable frequencies,
rendering the main signal useless. Curiously, the counter-interference (interference

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=184 ---

**157** Chapter 6 – Wireless LAN Organizations and Standards

provided by the wireless LAN interfering with Bluetooth) does not impact the Bluetooth
devices as severely as Bluetooth impacts the 802.11 compliant wireless LAN. It is now
common for placards to be mounted in wireless LAN areas that read “No Bluetooth” in
eye-catching print.

Bluetooth devices operate in three power classes: 1 mW, 2.5 mW, and 100 mW.
Currently there are few if any implementations of Class 3 (100 mW) Bluetooth devices,
so range data is not readily available; however, Class 2 (2.5 mW) Bluetooth devices have
a maximum range of 10 meters (33 feet). Naturally, if extended ranged is desired, the use
of directional antennas is a possible solution, though most Bluetooth devices are mobile
devices.

**Infrared Data Association (IrDA)**

IrDA is not a standard like Bluetooth, HomeRF, and the 802.11 series of standards;
rather, IrDA is an organization. Founded in June of 1993, IrDA is a member-funded
organization whose charter is “to create an interoperable, low-cost, low-power, halfduplex, serial data interconnection standard that supports a walk-up point-to-point user
model that is adaptable to a wide range of computer devices.” Infrared data transmission
is known by most for its use in calculators, printers, some building-to-building and inroom computer networks, and now in handheld computers.

**Infrared**

Infrared (IR) is a light-based transmission technology and is not spread spectrum—spread
spectrum technologies all use RF radiation. IR devices can achieve a maximum data rate
of 4 Mbps at close range, but as a light-based technology, other sources of IR light can
interfere with IR transmissions. The typical data rate of an IR device is about 115 kbps,
which is good for exchanging data between handheld devices. An important advantage
of IR networks is that they do not interfere with spread spectrum RF networks. For this
reason, the two are complementary and can easily be used together.

**Security**

The security of IR devices is inherently excellent for two main reasons. First, IR cannot
travel though walls at such a low power (2 mW maximum) and second, a hacker or
eavesdropper must directly intercept the beam in order to gain access to the information
being transferred. Single room networks that need wireless connectivity must be assured
of security benefit from IR networks. With PDAs and laptop computers, IR is used for
point-to-point connectivity at very short range so security would be almost irrelevant in
these instances.

**Stability**

Though IR will not pass through walls, it will bounce off walls and ceilings, which aids
in single room networking. Infrared is not disrupted by electromagnetic signals, which
promotes the stability of an IR system. Broadcast IR devices are available and can be
mounted on the ceiling. An IR broadcast device (which is analogous to an RF antenna)
will transmit the IR carrier and information in all directions so that these signals can be

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=185 ---

Chapter 6 – Wireless LAN Organizations and Standards **158**

picked up by nearby IR clients. For power consumption reason, broadcast IR is normally
implemented indoors for power reasons. Point-to-point IR transmitters can be used
outdoors, and have a maximum range of 1 km (about 3280 feet), but this range may be
shortened by the presence of sunlight. Sunlight is approximately 60% infrared light,
which severely dilutes broadcast IR signals. On sunny days when transferring data
between laptop computers or PDAs, the two devices may have to be held closer together
for good IR data transfer.

**Wireless LAN Interoperability Forum (WLIF)**

The OpenAir standard was a standard created by the Wireless LAN Interoperability
Forum (now defunct), for which many wireless LAN systems were created to comply as
an alternative to 802.11. OpenAir specified two speeds - 800 kbps and 1.6 Mbps.
OpenAir and 802.11 systems are not compatible and will not interoperate. Since there
are currently several product lines still available that comply with the OpenAir standard,
it is important that the wireless LAN administrator know that OpenAir exists; however,
OpenAir is quickly losing support among vendors and no new products are being made
that comply with this standard. OpenAir was the first attempt at interoperability and
standardization among wireless LANs. OpenAir focused on FHSS devices operating at
only two speeds.

![](images/06-organizations-and-standards.pdf-186-0.png)

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=186 ---

**159** Chapter 6 – Wireless LAN Organizations and Standards

##### Key Terms

Before taking the exam, you should be familiar with the following terms:

_infrared_

_ISM bands_

_UNII bands_

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=187 ---

Chapter 6 – Wireless LAN Organizations and Standards **160**

##### Review Questions

1. What data rates does the 802.11 standard specify when using DSSS?

A. 1 Mbps only

B. 2 Mbps only

C. 4 Mbps only

D. 1 & 2 Mbps

E. 1, 2, & 4 Mbps

2. The three UNII bands used for wireless LANs are each how wide?

A. 100 MHz

B. 102 MHz

C. 110 MHz

D. 120 MHz

3. The FCC specifies rules for wireless LANs regarding which of the following?
Choose all that apply.

A. Power output

B. Frequencies

C. Modulation

D. Data rates

4. Which of the following is NOT one of the ISM bands used with wireless LANs?
Choose all that apply.

A. 900 MHz

B. 2.4 MHz

C. 4.5 GHz

D. 5.8 GHz

5. The 802.11b standard specifies which of the following data rates using DSSS
technology?

A. 1 & 2 Mbps

B. 5.5 & 11 Mbps

C. 1, 2, & 11 Mbps

D. 1, 2, 5.5, & 11 Mbps

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=188 ---

**161** Chapter 6 – Wireless LAN Organizations and Standards

6. The 802.11b standard specifies which of the following spread spectrum
technologies?

A. FHSS

B. DSSS

C. Infrared

D. Key hopping

7. Which of the following standards specifies use of FHSS technology?

A. 802.11

B. 802.11b

C. 802.11a

D. 802.11g

E. OpenAir

8. What is the FCC limit on EIRP for a point-to-multipoint link?

A. 1 Watt

B. 2 Watts

C. 3 Watts

D. 4 Watts

9. Why are 802.11a devices incompatible with all other 802.11 family devices?

A. 802.11a devices operate at a maximum of 54 Mbps

B. 802.11a devices operate in the 5 GHz ISM band

C. 802.11a devices operate in the 5 GHz UNII bands

D. 802.11a devices use Barker Code modulation

10. Which of the following statements are true? Choose all that apply.

A. The IEEE is government regulated

B. The FCC is a government agency

C. The IEEE sets the allowable RF power outputs in the United States

D. The FCC specifies connectivity speeds for the 802.11 standard

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=189 ---

Chapter 6 – Wireless LAN Organizations and Standards **162**

11. What does the Wi-Fi™ seal of approval indicate?

A. A vendor’s hardware has a WECA chipset in it

B. A vendor’s hardware has been proven interoperable with other vendor’s
hardware

C. A wireless LAN meets the IEEE 802.11 standard

D. A wireless LAN meets FCC regulations

12. Which organization creates the regulations that wireless LANs must abide by?

A. IEEE

B. FCC

C. WECA

D. WLANA

13. You have been hired to take over the administration of a wireless LAN on a small
college campus. The campus uses one omni-directional antenna to connect 6
buildings. One day an inspector with the FCC tells you that the power output at the
element of your antenna is too high and violating FCC laws. What is the maximum
power output at which you can set the EIRP to comply with the law?

A. 125 mW

B. 1 W

C. 2 W

D. 4W

14. The FCC's jurisdiction covers which of the following? Choose all that apply.

A. The 50 United States only

B. The 50 United States and the District of Columbia

C. The 50 United States, the District of Columbia, and all U.S. possessions such as
Puerto Rico, Guam, and the Virgin Islands

D. All of Europe

15. Which one of the following is a disadvantage of a license-free radio frequency band?

A. No licensing fees or paperwork

B. Regulation by the FCC in the US

C. Possible random interference with other networks

D. Lower cost of equipment

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=190 ---

**163** Chapter 6 – Wireless LAN Organizations and Standards

16. "ISM" stands for which one of the following?

A. International Scientific Measurement

B. International Standards Makers

C. Industrial Standard Machine

D. Industrial, Scientific, and Medical

17. Which one of the following does NOT specify equipment that uses the 2.4 GHz ISM
band?

A. 802.11

B. 802.11a

C. 802.11b

D. 802.11g

E. 802.1x

18. Which one of the following defines the acronym "UNII"?

A. Unlicensed National Information Invention

B. Unlicensed National Information Infrastructure

C. Unlicensed Nominal Information Infrastructure

D. Unlicensed National Innovation Infrastructure

19. Which one of the following is the key standards maker for most information
technology arenas in the United States?

A. WECA

B. FCC

C. IEEE

D. WLANA

E. IrDA

20. Which one of the following was the FIRST IEEE standard describing the operation
of wireless LANs?

A. 802.11

B. 802.11a

C. 802.11b

D. 802.11g

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=191 ---

Chapter 6 – Wireless LAN Organizations and Standards **164**

##### Answers to Review Questions

1. D. The 802.11 standard specifies data rates for FHSS, DSSS, and infrared
technologies. The two speeds specified by the 802.11 standard are 1 Mbps and 2
Mbps. Speeds for DSSS were thereafter amended with the 802.11b standard to add
both 5.5 & 11 Mbps speeds.

2. A. Each of the three 5 GHz UNII bands are exactly 100 MHz wide. The lower band
ranges from 5.15 - 5.25 GHz. The middle band ranges from 5.25 - 5.35 GHz. The
upper band ranges from 5.725 - 5.825 GHz.

3. A, B. The FCC mandates which frequencies may be used for what purposes. They
specify which frequency bands will be licensed or unlicensed, and they specify the
maximum output power within each frequency band.

4. B, C. Note that the most popular ISM band in use today is the 2.4 **GHz** ISM band,
not the 2.4 **MHz** ISM band. There are three ISM bands specified by the FCC. The
first is the 902 - 928 MHz band. The second is the 2.4000 - 2.5000 GHz band, and
the third is the 5.825 - 5.875 GHz band.

5. D. Although the most significant changes from the original 802.11 standard was the
additional data rates of 5.5 & 11 Mbps, the 1 & 2 Mbps data rates are still specified
in 802.11b for backwards compatibility with the 802.11 standard.

6. B. The 802.11b standard only specifies use of DSSS technology. The original
802.11 standard specified use of DSSS, FHSS, and infrared technologies.

7. A, E. Both the original 802.11 and the OpenAir standards specified use of FHSS
technology. The most significant difference between these two standards is the
supported speeds. OpenAir specifies 800 kbps and 1.6 Mbps whereas 802.11
specifies 1 Mbps and 2 Mbps.

8. D. For point-to-multipoint links, the FCC specifies 1 watt at the intentional radiator
and 4 watts EIRP (measured at the antenna element). For point-to-point links, there
are specific, more complicated rules to follow to understand the maximum output
power allowed.

9. C. Since 802.11a devices use the three 5 GHz UNII bands, they cannot
communicate with other wireless LAN devices operating in accordance with the
802.11, 802.11b, and 802.11g standards. These standards use the 2.4 GHz ISM
band instead of the 5 GHz UNII bands.

10. B. The FCC is a government agency responsible for regulating frequency spectra
within the United States. As a part of that responsibility, the FCC regulates the
unlicensed bands used by wireless LANs.

11. B. The Wireless Fidelity (a.k.a. Wi-Fi) seal indicates that a vendor's hardware has
undergone extensive testing to assure interoperability with other devices
manufactured to meet the 802.11b standard. In order to be interoperable with other
802.11b equipment, the equipment under test would most likely have to meet the
same 802.11b standards.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=192 ---

**165** Chapter 6 – Wireless LAN Organizations and Standards

12. B. The FCC creates the regulations (laws) to which wireless LAN equipment must
adhere. The IEEE creates standards for the purpose of interoperability within the
industry. WECA creates the tests and certification program to assure
interoperability within the industry using specific standards. WLANA is responsible
for promoting and educating the wireless LAN industry.

13. D. The FCC mandates a 4 watt maximum EIRP in a point-to-multipoint circuit.
One important part of this rule is understanding that any time an omni-directional
antenna is used, the circuit is automatically considered point-to-multipoint.

14. C. Clicking on the "About the FCC" link on the homepage of the FCC
(www.fcc.gov) yields this information in the first paragraph.

15. C. It is said that the biggest advantage of using wireless LANs is that they are
license free. It is also said that the biggest disadvantage to using wireless LANs is
that they are license free. Sometimes the fact that nearby license-free networks
interfere with yours seems to outweigh the implementation ease and cost factors of
the frequency spectrum being license free.

16. D. The FCC created the ISM bands with specific industry uses in mind: Industrial,
Scientific, and Medical related uses. However, since the availability of the ISM
bands, license-free wireless LAN gear has enjoyed broad popularity and diverse use.

17. B, E. The 802.1x standard is centered on port-based access control. This standard
can be used to enhance the security of wireless systems, but is not a wireless LAN
standard itself. The 802.11a standard specifies use of the 5 GHz UNII bands.

18. B. There are three UNII bands, all specified for use by various 802.11a compliant
devices. These three UNII bands are 100 MHz wide and each have different
maximum output power limits and usage requirements.

19. C. The IEEE creates standards for most every type of connectivity, whether wired
or wireless. The IEEE's role in keeping each information technology industry
working within certain standards is quite important to rapid advancement of the
industry.

20. A. The original 802.11 standard was started in 1990 and finished in 1997. It
underwent several revisions after 1997, the final being the 1999 revision. Since the
1999 version of 802.11, there have been several new 802.11-based standards
published by the IEEE such as 802.11b and 802.11a. Several more drafts related to
wireless LANs are currently on their way to becoming standards such as 802.11i,
802.11g, and 802.11f.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=193 ---

--- end of page=194 ---
