# Appendix A - RF in Perspective

_PDF pages 370-375_

##### RF in Perspective

Throughout this book, we have provided the technical facts, specifications,
and many "how to" descriptions of wireless LANs; however, without
experience working with RF networks, it may still be difficult to understand
the big picture. You will spend many hours in trial and error when working
with RF networks, and skill comes with experience. The following RF
Primer should help dispel some common misconceptions about wireless
LANs and explain in simple terms some of the scenarios involved with
forming wireless connections and optimizing wireless LAN links.
Appropriate use of hardware, antenna gain, amplification, antenna use,
receiver sensitivity, output power, and FCC regulations are all addressed
in hopes that you will get a good perspective of what working with wireless
LANs involves.

This RF Primer was authored by Michael F. Young of Young Design, Inc.
[(www.ydi.com), and edited by Planet3 Wireless, Inc., for use within the](http://www.ydi.com/)
CWNA Study Guide.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

CHAPTER APPENDIX
# 5 A

**In This Chapter**

Radio acts like light

Light bulb analogy

Transmit Range Tests

Receive range tests

Obstacles

Fresnel Zone

Increasing power at the
tower

Reflection

--- end of page=369 ---

Appendix A – RF in Perspective **342**

##### RF in Perspective

**Radio acts like light**

For people who have no RF experience, it may be difficult to visualize how radio waves
travel, or propagate, through the air. Even for those with RF experience, this concept is
sometimes difficult to understand. An easy way to think about microwave signals
(generally those frequencies above 1000 MHz or 1 GHz) is to use light as an analogy.
Light is an electromagnetic signal as are radio frequency waves.

**Light bulb analogy**

For purposes of this light-radio analogy, we will create a hypothetical example that
should help the thought process of understanding radio frequency. Imagine a dark,
overcast night sky with no moon or stars shining through the high clouds, away from any
city lights, where the area is totally pitch black, but closer to the ground visibility is clear.
If one were to disassemble the light mechanism and remove the reflective mirror from
behind the bulb of a standard flashlight with two D-cell batteries, and then set it up so
that the light bulb is hanging in free space, the bulb lights up the room, but there is not
even enough light to read by.

The power output of this bulb is only about 2 watts. In the license-free 2.4 GHz radio
band, the most power that the FCC allows for powering an omni-directional antenna is 1
watt.

If half of the light’s power is removed by removing one of the two batteries, the intensity
of the bulb drops considerably. The light’s output decreases because the power output is
proportional to the square of the voltage, meaning that, if the voltage is cut in half, the
power goes down by 25%.

The next part of the analogy is to imagine installing this 1 watt light on a tall radio tower,
mountaintop, or tall building. The amount of light output represents roughly the radiation
power that is present with an amplifier feeding a 6 dBi (decibel) gain omni-directional
antenna.

**Transmit Range Tests**

At a distance of approximately ½ mile from this hypothetical tower, one should be able to
see the light with the naked eye, but just barely. This arrangement using the naked eye
would be analogous to a low-gain dipole antenna.

At a distance of a mile or two away, one will not likely be able to see the bulb anymore.
Using a X10 (times ten) telescope and aiming it at the bulb on the tower, the light bulb is
now visible. This layout would be analogous to using a 10 dBi gain directional antenna,
such as a flat panel or Yagi antenna. A 10 dBi gain antenna has about ten times the
focusing gain of a simple whip, or dipole, antenna.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=370 ---

**343** Appendix A – RF in Perspective

From a distance of five or six miles out, the light is so weak that even the X10 scope
cannot see it. Using a X100 scope, the light comes in clearly, but the viewing area of the
telescope is much smaller, which makes aiming the telescope (analogous to an antenna)
properly even more critical. This setup would be comparable to using a 20 dBi dish
antenna. A 20 dBi gain directional antenna has nearly 100 times the focusing power of a
dipole antenna.

From a distance of ten miles or more, presuming that the bulb is mounted high enough up
so that there is clear line of sight back to it, even the X100 scope does not see the bulb. If
one were to use a X100 night scope, like the ones that military and law enforcement use,
the bulb would now be clearly visible, but so would everything around the bulb and the
background (“background noise” as infrared light). This configuration is analogous to
using a radio amplifier at the client site, which, in this example, would be where the highpowered night scope is.

In order for the bulb to be brighter, the brightness control (gain) on the night scope can be
increased. As the bulb gets brighter through the night scope, so does all the background
light. If the brightness control is turned up full, the light from the bulb is overcome by all
the background noise created by the light amplification circuitry and the light itself gets
lost in this background light.

If the gain on the night scope is turned down to the point at which the bulb is as bright as
possible without an intolerable increase in the background light, this point represents the
optimum “signal-to-noise” ratio for this particular configuration. Turning up the
brightness (gain) did not improve the visibility of the bulb, but instead, stressed the
viewer’s eyes and made the viewer’s iris close up to compensate for the increase in the
overall light level caused by the increased brightness (gain).

The lesson from this situation is: use only as much receiver gain as is necessary because
too much gain can cause less than optimum results. A delicate balance exists within the
ratio of the signal to the noise when working with radio frequency.

**Receive range tests**

The above example explained the analysis of what the client side of the RF link would
see. Below, we will look in the other direction of the signal: what the unit on the tower
would see. A wireless LAN requires two-way communication, and connectivity is
impossible if the client can see the tower’s signal, but the tower cannot see the client’s
signal.

Continuing with the light analogy, if the voltage to the bulb is decreased so that, instead
of radiating 1 watt, it puts out fifty-thousandths of a watt (50 mW), barely lighting the
filament. Fifty milliwatts is equivalent to the transmitter power emitted by typical
wireless LAN cards and access points. At this level of power, the bulb cannot be seen
past several hundred feet away. Using the same X100 night scope mentioned earlier, the
bulb is visible. The night scope will be the viewing mechanism, representing an
amplifier, for the remainder of this example.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=371 ---

Appendix A – RF in Perspective **344**

At a distance of a half-mile, the bare bulb can be seen with a properly adjusted night
scope.

At a mile or two away, the bare bulb is not visible because the light’s intensity is too
weak. If the bulb is setup behind an X10 telescope eyepiece, so that the X10 eyepiece is
aimed back up at the tower, this setup would be equivalent to feeding the radio signal into
a directional high-gain antenna. With the X10 telescope aimed towards the tower, the
bulb is visible from the tower’s X100 night scope.

At five miles out, the X100 telescope is necessary in order for the client on the tower to
see the bulb. The light is not strong, but it is visible. At ten miles, the bulb is not visible
at all, so the voltage feeding the bulb is increased. The bulb is now radiating 250
milliwatts, which represents the maximum the FCC allows into a 24 dBi gain dish
antenna. The bare bulb is still not visible from the tower. With the X10 scope in front of
the bulb, the light is visible, but it is not strong. With the X100 telescope, the light is
quite bright.

The lesson here is that high-gain directional antennas are needed at the client end of a
wireless link.

**Obstacles**

If there were any obstacles in the way, the bulb would not be visible. This situation is
one area in which the light bulb analogy begins to break down. A 2.4 GHz radio signal
will go through walls and floors - light will not. How many walls and floors the radio
signal will go through depends on the type and the thickness of the material of the walls.
RF signals easily travel through sheet rock walls, such as those found in offices and
homes, but are seriously attenuated (weakened) through steel reinforced concrete walls
and floors.

At long distances, the analogy holds up. A large building in the way will definitely block
the radio signal. At close range (a mile or less), reflection and/or refraction of the radio
signal will possibly allow connectivity, but that connectivity is both unpredictable and
unreliable.

**Fresnel Zone**

The other departure from our light analogy is the concept of the Fresnel Zone. Radio
waves, unlike light, do not travel in thin laser-like lines. RF waves emanate away from
an antenna like ripples in a pond when a rock is thrown in. Radio waves fan out,
becoming wider toward the middle of the link. The area where radio waves spread out is
called the Fresnel Zone. Light actually has a Fresnel Zone, but because its wavelength is
so small, the Fresnel Zone is microscopic. It is possible to have a situation in which there
is clear or laser-like line of sight back to the base antenna, but no radio connectivity.
Examples of this situation are if the base antenna is visible through a slit between two
nearby buildings in the way, or if the tower is just barely visible in the distance over the
visual horizon or obstacle. In both cases, the Fresnel Zone is encroached upon and the
signal in both directions will be attenuated.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=372 ---

**345** Appendix A – RF in Perspective

Depending on the distance involved and the amount of the Fresnel Zone that is
encroached upon, a radio link may not be possible.

**Increasing power at the tower**

Wireless LAN users frequently want high-power amplifiers (for use at a tower) that
exceed FCC Part 15 regulations. When asked why, they reply, "Because we want a
strong signal to reach our clients.” When asked if they intend to put amplifiers at their
clients’ sites, they invariably say “no.” The next step for the wireless LAN expert is to
point out that it makes no sense to put several watts of transmit power at the tower site
while their clients only have perhaps 30 milliwatts of transmit power. Since a wireless
LAN is a two-way system, if the base cannot hear the weak client, it does not matter how
strong the signal from the base is. There must be amplification at both ends for a
balanced system.

**Reflection**

In cases where the client is located close to the base station, it is possible to get a non line
of sight connection off of a reflection from a nearby building. Once again, if everything
is very close together (less than 1000 feet), the weak reflection from the building may
have enough “illumination” to be captured by a high-gain antenna aimed at the reflecting
point.

**RF Summary**

Below are several points to remember when implementing wireless links.

      - Antennas, like telescopes, focus the signal and offer the same gain for both
transmitted and received signals.

      - The tower should always use an amplifier.

      - Clients (except those in close proximity to the tower) need to use high-gain
directional antennas when possible.

      - Clients at a distance from the tower may need amplifiers.

      - Clear, unobstructed line of sight is required, except perhaps for clients in close
proximity to the tower.

      - Fresnel Zone encroachment will reduce the strength of the radio signal.

      - It is illegal, per FCC Part 15 regulations, to implement a wireless LAN that is not
certified. Violation of FCC regulations can result in fines, imprisonment, and
confiscation of the wireless link that violates the regulations.

      - Reflected signals may be strong enough if the distances are short.

CWNA Study Guide © Copyright 2002 Planet3 Wireless, Inc.

--- end of page=373 ---

--- end of page=374 ---
