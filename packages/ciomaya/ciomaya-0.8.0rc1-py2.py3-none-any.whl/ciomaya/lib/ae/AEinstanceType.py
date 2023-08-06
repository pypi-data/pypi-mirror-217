from __future__ import unicode_literals

"""
Handle the UI for instanceTypes:

"""

import maya.app.renderSetup.model.renderSetup as rs
import maya.app.renderSetup.views.overrideUtils as ov_utils
import pymel.core as pm
from ciocore import data as coredata

from ciomaya.lib import const as k
from ciomaya.lib.ae import AEcommon


def create_ui(node_attr):
    """Build static UI

    Components:

    1. Category menu - for example: "CPU", "GPU", "High Tier", "Low Tier"
    2. Content menu is efectively as submenu of categories - for example: "c4.8xlarge", "g2.2xlarge", "m4.2xlarge"
    3. Popup menu - contains: "Create Absolute Override for Visible Layer"
    """
    with AEcommon.ae_template():
        pm.rowLayout(
            numberOfColumns=3,
            columnWidth3=(k.AE_TEXT_WIDTH, 100, 300),
            columnAttach=((1, "both", 0), (2, "both", 0), (3, "both", 0)),
        )

        label = pm.text("instanceTypesLabel", label="Instance Type")
        pm.optionMenu("instanceTypesCategoryMenu", acc=True)
        pm.optionMenu("instanceTypesContentMenu", acc=True)

        popup = pm.popupMenu(parent=label)
        pm.setParent(popup, menu=True)
        pm.menuItem(label="Create Absolute Override for Visible Layer")
        pm.setParent("..")  # out of rowLayout

        populate_ui(node_attr)


def populate_ui(node_attr):
    """Rehydrate the UI for the current node.attribute.

    This is called when the UI is first created, and when switching to a different submitter.
    """
    attr = pm.Attribute(node_attr)
    widgets = _get_widgets()

    if not coredata.valid():
        for item in pm.optionMenu(widgets["contentmenu"], q=True, itemListLong=True):
            pm.deleteUI(item)
        pm.setParent(widgets["contentmenu"], menu=True)
        pm.menuItem(label="Not connected")
        for item in pm.optionMenu(widgets["catmenu"], q=True, itemListLong=True):
            pm.deleteUI(item)
        pm.setParent(widgets["catmenu"], menu=True)
        pm.menuItem(label="---")
    # update popup menu items
    _configure_popup_menu(attr, widgets)

    pm.optionMenu(
        widgets["catmenu"],
        edit=True,
        changeCommand=pm.Callback(_on_category_menu_change, attr, widgets),
    )
    pm.optionMenu(
        widgets["contentmenu"],
        edit=True,
        changeCommand=pm.Callback(_on_content_menu_change, attr, widgets["contentmenu"]),
    )

    # Update this UI if the attribute changes by some other means
    # For example: setAttr, or another instance of the attribute editor.
    _setup_script_jobs(attr, widgets)
    _set_label_color(attr, widgets["label"])

    pm.evalDeferred(pm.Callback(_ensure_connection, attr, widgets))

### Private

def _configure_popup_menu(attr, widgets):
    override_item = pm.popupMenu(widgets["popup_menu"], q=True, itemArray=True)[0]

    enable_override = (
        pm.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        != "defaultRenderLayer"
    )
    pm.menuItem(
        override_item,
        edit=True,
        en=enable_override,
        command=pm.Callback(_create_layer_override, attr, widgets["label"]),
    )


def _get_widgets(parent=None):
    if not parent:
        parent = pm.setParent(q=True)
    label = AEcommon.find_ui("instanceTypesLabel", parent),
    return {
        "label": label,
        "catmenu": AEcommon.find_ui("instanceTypesCategoryMenu", parent),
        "contentmenu": AEcommon.find_ui("instanceTypesContentMenu", parent),
        "popup_menu": pm.control(label, q=True, popupMenuArray=True)[0],
    }


def _setup_script_jobs(attr, widgets):
    """
    Update the UI based on events.

    1. When the attribute changes - sync the menu to the attribute value.
    2. When the render layer manager changes - sync the menu and update the label color.
    """
    menu = widgets["contentmenu"]

    pm.scriptJob(
        attributeChange=(
            attr,
            pm.Callback(_sync_menu_to_attr, attr, widgets),
        ),
        parent=menu,
        replacePrevious=True,
    )

    pm.scriptJob(
        event=(
            "renderLayerManagerChange",
            pm.Callback(_on_render_layer_manager_change, attr, widgets),
        ),
        parent=menu,
    )


def _on_render_layer_manager_change(attr, widgets):
    _sync_menu_to_attr(attr, widgets)
    _set_label_color(attr, widgets["label"])


def _ensure_connection(attr, widgets):
    """Fetch a fresh list of inst types from Conductor (or the cache)

     hardware.categories are expected to be structured like this:

    [
        {
            "label": "Category 1",
            "content": [
                {"description": "Content 1", "name": "content1", and-so-on ...},
                {"description": "Content 2", "name": "content2", and-so-on ...},
                {"description": "Content 3", "name": "content3", and-so-on ...}
            ]
        },
        {
            "label": "Category 2",
            "content": [
                {"description": "Content 4", "name": "content4", and-so-on ...},
                {"description": "Content 5", "name": "content5", and-so-on ...},
                {"description": "Content 6", "name": "content6", and-so-on ...}
            ]
        }
    ]
    """

    hardware = coredata.data().get("instance_types")
    if not hardware:
        return

    category_labels = [item["label"] for item in hardware.categories]
    if not category_labels:
        return
    AEcommon.ensure_populate_menu(widgets["catmenu"], category_labels)
    _sync_menu_to_attr(attr, widgets)


def _sync_menu_to_attr(attr, widgets):
    """
    Make sure menu item reflects the attribute value.

    If the attribute is invalid, set it to the first valid project.
    """

    attr_value = attr.get()
    hardware = coredata.data()["instance_types"]
    instance_type = hardware.find(attr_value)

    if not instance_type:
        # list must have changed or attribute is invalid
        instance_type = hardware.find_first(lambda x: x["cores"] > 2)
        attr_value = instance_type["name"]
        attr.set(attr_value)
        AEcommon.print_setAttr_cmd(attr)
    category_label = instance_type["categories"][0]["label"]
    # set the category menu to the first category that contains the sku
    pm.optionMenu(widgets["catmenu"], edit=True, value=category_label)
    category = hardware.find_category(category_label)
    if not category:
        pm.displayWarning(
            "Didn't find category '{}' in instance types".format(category_label)
        )
        return
    content_descriptions = [c["description"] for c in category["content"]]
    AEcommon.ensure_populate_menu(widgets["contentmenu"], content_descriptions)
    pm.optionMenu(widgets["contentmenu"], edit=True, value=instance_type["description"])

    _set_label_color(attr, widgets["label"])


def _on_category_menu_change(attr, widgets):
    hardware = coredata.data()["instance_types"]
    num_items = pm.optionMenu(widgets["catmenu"], q=True, numberOfItems=True)
    if not num_items:
        return
    category_label = pm.optionMenu(widgets["catmenu"], q=True, value=True)
    category = hardware.find_category(category_label)
    if not category:
        pm.displayWarning(
            "Didn't find category '{}' in instance types".format(category_label)
        )
        return
    content_labels = [c["description"] for c in category["content"]]

    AEcommon.ensure_populate_menu(widgets["contentmenu"], content_labels)
    attr_value = attr.get()
    instance_type = hardware.find(attr_value)
    if not category_label in [c["label"] for c in instance_type["categories"]]:
        instance_type = category["content"][0]
        attr_value = instance_type["name"]
        attr.set(attr_value)
        AEcommon.print_setAttr_cmd(attr)

    pm.optionMenu(widgets["contentmenu"], edit=True, value=instance_type["description"])


def _on_content_menu_change(attr, menu):
    """
    Respond to menu change.

    Set the value of the attribute to the selected item.
    """
    hardware = coredata.data()["instance_types"]
    num_items = pm.optionMenu(menu, q=True, numberOfItems=True)
    if not num_items:
        return
    label = pm.optionMenu(menu, q=True, value=True)
    instance_type = hardware.find_first(lambda x: x["description"] == label)

    if not instance_type:
        pm.displayWarning("Didn't find '{}' in instance types".format(label))
        return

    name = instance_type["name"]
    if attr.get() != name:
        attr.set(name)
        AEcommon.print_setAttr_cmd(attr)


def _create_layer_override(attr, label):
    ov_utils.createAbsoluteOverride(attr.node().name(), attr.attrName(True))
    _set_label_color(attr, label)


def _set_label_color(attr, label):
    """By convention, label is orange if attr has an override."""
    has_override = rs.hasOverrideApplied(attr.node().name(), attr.attrName(True))
    text = "Instance Type Name"
    label_text = "<font color=#ec6a17>{}</font>".format(text) if has_override else text
    pm.text(label, edit=True, label=label_text)
