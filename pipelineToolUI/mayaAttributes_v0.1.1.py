
_IN_MAYA_ = False

try:
    from maya import cmds
    
    _IN_MAYA_ = True
except:
    print("PAS DANS MAYA")

class MayaAttributes():

    def attributeCreate(self, name, value, type, on):
        """This function allows to create and replace attributes
        of type string, integer or float on shapes and transforms.

        Args:
            name (string): This is the name of the attribute.
            value (string or int): This is the value of the attribute.
            type (string): This is the type of the attribute.
            on (string): This define if we want add attribute on shapes or transforms.
        """
        
        mySel = cmds.ls(sl = True)                                                                          # Get the current selection.

        if(on == 'Transform'):                                                                              # if we want to add attribute on Transforms condition.
            for each in mySel:                                                                              # For loop on the current selection.
                                                                                                            # Query if the attribute existing.
                existing_attrib         = cmds.attributeQuery(name, node = each, exists = True)
                
                if not existing_attrib:                                                                     # If the attribute not existing condition.
                    if(type == 'string'):                                                                   # If the type attribute is 'string' condition.
                        createAttr      = cmds.addAttr(each, shortName = name, longName = name, dt = type)  # Create attribute of type string on Transform.
                        setAttri        = cmds.setAttr(each + '.' + name, value, type = type)               # Set the attribute.
                    else:
                        createAttr      = cmds.addAttr(each, shortName = name, longName = name, at = type)  # Create attribute of type integer and float on Transform.
                        setAttri        = cmds.setAttr(each + '.' + name, value)                            # Set the attributes.
                    
                else:                                                                                       # If the attribute existing.
                    if(type == 'string'):                                                                   # If the type attribute is 'string' condition.
                        setAttri        = cmds.setAttr(each + '.' + name, value, type = type)               # Set the attribute of type string on Transform.
                    else:
                        setAttri        = cmds.setAttr(each + '.' + name, value)                            # Set the attribute of type int or float on Transform.

        else:                                                                                               # If we want to add attribute on Shapes condition.
            shapes = cmds.listRelatives(shapes = True)
            if(not shapes):
                pass
            else:                
                for each2 in shapes:                                                                        # For loop on shapes list.
                    existing_attrib     = cmds.attributeQuery(name, node = each2, exists = True)
                    
                    if not existing_attrib:                                                                 # All the same things that for Transforms attributes but on Shapes.
                        if(type == 'string'):
                            createAttr  = cmds.addAttr(each2, shortName = name, longName = name, dt = type)
                            setAttri    = cmds.setAttr(each2 + '.' + name, value, type = type)
                        else:
                            createAttr  = cmds.addAttr(each2, shortName = name, longName = name, at = type)
                            setAttri    = cmds.setAttr(each2 + '.' + name, value)
                    else:
                        if(type == 'string'):
                            setAttri    = cmds.setAttr(each2 + '.' + name, value, type = type)
                        else:
                            setAttri    = cmds.setAttr(each2 + '.' + name, value)
    

    def attributeDelete(self, attrName, on):
        """This function allows to delete the attribute who is
        enter in the attribute name line edit of the interface
        and work on the current selection.

        Args:
            attrName (string)   : This is the name of the attribute.
            on (string)         : This define if we want add attribute on shapes or transforms.
        """

        mySel = cmds.ls(sl = True)

        if(on == 'Transform'):                                                                              # if we want to add attribute on Transforms condition.
            for each in mySel:                                                                              # For loop on the current selection.
                                                                                                            # Query if the attribute existing.
                existing_attrib         = cmds.attributeQuery(attrName, node = each, exists = True)
                
                if not existing_attrib:                                                                     # If the attribute not existing condition.
                    pass

                else:                                                                                       # If the attribute existing.
                    cmds.deleteAttr(each, name = each, at = attrName)

        else:                                                                                               # If we want to add attribute on Shapes condition.
            shapes = cmds.listRelatives(shapes = True)

            if(not shapes):
                pass
            else:                
                for each2 in shapes:                                                                        # For loop on shapes list.

                    existing_attrib     = cmds.attributeQuery(attrName, node = each2, exists = True)
                    
                    if not existing_attrib:                                                                 # All the same things that for Transforms attributes but on Shapes.
                        pass
                    else:
                        cmds.deleteAttr(each2, name = each2, at = attrName)