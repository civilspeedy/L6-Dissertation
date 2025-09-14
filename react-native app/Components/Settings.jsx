/**
 * @file A file housing components that make up the settings modal.
 * @module Settings
 */
import { useEffect, useState } from 'react';
import {
    Modal,
    Pressable,
    View,
    Text,
    StyleSheet,
    Switch,
    KeyboardAvoidingView,
} from 'react-native';
import { BlurView } from 'expo-blur';
import { Feather } from '@expo/vector-icons';
import NameEntry, { checkNameInput } from './Name Entry';
import { getLocationAccess, setLocationAccess } from '../Logic/Manipulation';
import getLocationAndPerm from '../Logic/Location';
import { impactAsync } from 'expo-haptics';

/**
 * A modal for changing the user's desired name and location permission.
 * @param {object} activeTheme an object containing values for the current theme.
 * @returns {View} a modal wrapped in a view, the modal is triggered to open upon a button press.
 */
export default function Settings({ activeTheme }) {
    const [state, setState] = useState(false);
    const [newName, setNewName] = useState('');
    const [access, setAccess] = useState(false);

    useEffect(() => {
        /**
         * Fetches from storage where access to the user's device location has been granted.
         */
        const fetchLocationAcc = async () => {
            const fetchedLocation = await getLocationAccess();
            setAccess(fetchedLocation);
        };

        fetchLocationAcc();
    }, []);

    useEffect(() => {
        setLocationAccess(access);
        if (access == true) {
            getLocationAndPerm();
        }
    }, [access]);

    /**
     * A function for handle to two types of closing the settings page: with or without saving.
     * @param {boolean} save whether the user wants to save the changes or not.
     */
    const handleClose = (save) => {
        if (save) {
            if (newName == '') {
                setState(false);
            } else if (checkNameInput(newName)) {
                setNewName('');
                setState(false);
            } else {
                setNewName('');
            }
        } else {
            setNewName('');
            setState(false);
        }
    };

    return (
        <View>
            <Modal
                transparent={true}
                visible={state}
                animationType='fade'>
                <BlurView
                    style={styles.blurView}
                    tint='systemThinMaterial'
                    intensity={80}>
                    <KeyboardAvoidingView
                        behavior='height'
                        style={{ flex: 1 }}
                        keyboardVerticalOffset={20}>
                        <View
                            style={[
                                styles.modalContent,
                                { backgroundColor: activeTheme.modalColour },
                            ]}>
                            <Text style={[styles.font, { marginBottom: 10 }]}>
                                Change Name:{' '}
                            </Text>
                            <NameEntry
                                name={newName}
                                setName={setNewName}
                            />
                            <View style={styles.locationView}>
                                <Text style={styles.font}>
                                    Allow Location Services:{' '}
                                </Text>
                                <Switch
                                    trackColor={{
                                        true: 'lightgreen',
                                        false: 'red',
                                    }}
                                    onValueChange={setAccess}
                                    value={access}
                                    style={{
                                        marginLeft: 10,
                                    }}
                                    shouldRasterizeIOS={true}
                                />
                            </View>
                            <View style={styles.buttonsView}>
                                <Pressable
                                    onPress={() => handleClose(true)}
                                    style={[
                                        styles.closeButtons,
                                        { backgroundColor: 'lightgreen' },
                                    ]}>
                                    <Text style={styles.font}>Save</Text>
                                </Pressable>

                                <Pressable
                                    style={[
                                        styles.closeButtons,
                                        { backgroundColor: 'salmon' },
                                    ]}
                                    onPress={() => handleClose(false)}>
                                    <Text style={styles.font}>Discard</Text>
                                </Pressable>
                            </View>
                        </View>
                    </KeyboardAvoidingView>
                </BlurView>
            </Modal>

            <Pressable
                style={[
                    styles.button,
                    { backgroundColor: activeTheme.secondary },
                ]}
                onPress={() => {
                    setState(true);
                    impactAsync();
                }}>
                <Feather
                    name='settings'
                    size={50}
                    color={activeTheme.primary}
                />
            </Pressable>
        </View>
    );
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    blurView: {
        flex: 1,
    },
    button: {
        position: 'absolute',
        top: 10,
        left: 10,
        padding: 5,
        borderRadius: 50,
        margin: 20,
    },
    closeButtons: {
        textAlign: 'center',
        justifyContent: 'center',
        padding: 20,
        marginBottom: 10,
        borderRadius: 50,
        borderWidth: 3,
    },
    modalContent: {
        alignItems: 'center',
        justifyContent: 'center',
        alignContent: 'center',
        marginTop: '40%',
        marginHorizontal: 20,
        height: '60%',
        borderRadius: 50,
    },
    textInput: {
        borderWidth: 3,
        borderRadius: 50,
        width: '80%',
        height: '10%',
    },
    locationView: {
        flexDirection: 'row',
        margin: 10,
        alignItems: 'center',
    },
    buttonsView: {
        margin: 10,
    },
    font: {
        textAlign: 'center',
        fontSize: 16,
        fontWeight: 'bold',
    },
});
