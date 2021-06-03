import gdspy

from mask.elements.test import VanDerPauwMetal, VanDerPauwContact, CTLMContact

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
        contactw=CONTACT, contactspacing=SPACING
    )
    vdp_contact = VanDerPauwContact(
        lib, 'VDPContact',
        contactw=CONTACT, contactspacing=SPACING, overhang=OVERHANG
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

    y +=  vdp_metal.height+400

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

    x +=  vdp_metal.width+400


    return testset_vert, testset_hor
