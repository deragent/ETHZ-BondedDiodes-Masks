import gdspy

from mask.elements.test import VanDerPauwMetal, VanDerPauwContact, CTLMContact, Resolution

CONTACT = 100
OVERHANG = 10

SPACING = 400

def Run2_TestSet(lib):

    testset_vert = lib.new_cell('TEST_SET_VERTICAL')
    testset_hor = lib.new_cell('TEST_SET_HORIZONTAL')

    ctlm_contact = CTLMContact(
        lib, 'CTLM_CONTACT',
        [8, 16, 24, 32, 40, 48, 64, 80, 96], (3, 3),
        radius_i=CONTACT, size=SPACING
    )

    ctlm_none = CTLMContact(
        lib, 'CTLM_NONE',
        [8, 16, 24, 32, 40, 48, 64, 80, 96], (3, 3),
        radius_i=CONTACT, size=SPACING,
        with_contact_implant=False
    )

    vdp_metal = VanDerPauwMetal(
        lib, 'VDPMetal',
        contactw=CONTACT*2, contactspacing=SPACING*1.5
    )
    vdp_contact = VanDerPauwContact(
        lib, 'VDPContact',
        contactw=CONTACT*2, contactspacing=SPACING*1.5, overhang=OVERHANG
    )

    resolution_metal = Resolution(
        lib, 'RESMetal',
        layer='METALIZATION', critical_dimension=5
    )
    resolution_implant = Resolution(
        lib, 'RESImplant',
        layer='CONTACT_DOPING', critical_dimension=5
    )

    ## Vertical
    y = 0
    testset_vert.add(gdspy.CellReference(ctlm_none.cell,
        origin=(0, y)))
    y +=  ctlm_none.height/2 + SPACING

    y +=  ctlm_contact.height/2
    testset_vert.add(gdspy.CellReference(ctlm_contact.cell,
        origin=(0,y)))
    y +=  ctlm_contact.height/2 + SPACING

    y +=  vdp_metal.height/2

    testset_vert.add(gdspy.CellReference(vdp_metal.cell, origin=(-(vdp_metal.width+SPACING)/2, y)))
    testset_vert.add(gdspy.CellReference(vdp_contact.cell, origin=(+(vdp_contact.width+SPACING)/2, y)))

    y +=  vdp_metal.height/2 + SPACING

    y += resolution_metal.height/2

    testset_vert.add(gdspy.CellReference(resolution_metal.cell, origin=(-(resolution_metal.width+SPACING)/2, y)))
    testset_vert.add(gdspy.CellReference(resolution_implant.cell, origin=(+(resolution_implant.width+SPACING)/2, y)))

    y += resolution_metal.height/2 + SPACING


    ## Horizontal
    x = 0
    testset_hor.add(gdspy.CellReference(ctlm_none.cell,
        origin=(x, 0)))
    x +=  ctlm_none.width/2 + SPACING

    x +=  ctlm_contact.width/2
    testset_hor.add(gdspy.CellReference(ctlm_contact.cell,
        origin=(x, 0)))
    x +=  ctlm_contact.width/2 + SPACING

    x +=  vdp_metal.width/2

    testset_hor.add(gdspy.CellReference(vdp_metal.cell, origin=(x, -(vdp_metal.height+SPACING)/2)))
    testset_hor.add(gdspy.CellReference(vdp_contact.cell, origin=(x, +(vdp_contact.height+SPACING)/2)))

    x +=  vdp_metal.width/2 + SPACING

    x += resolution_metal.width/2
    testset_hor.add(gdspy.CellReference(resolution_metal.cell, origin=(x, 0)))
    x += resolution_metal.width/2 + SPACING

    x += resolution_implant.width/2
    testset_hor.add(gdspy.CellReference(resolution_implant.cell, origin=(x, 0)))
    x += resolution_implant.width/2 + SPACING


    return testset_vert, testset_hor
