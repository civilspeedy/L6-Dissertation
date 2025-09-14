/**
 * @file Contains components that open on the first time the app is launched.
 * @module StarterPage
 */
import { useState, useEffect } from 'react';
import { Pressable, StyleSheet, Text, View, Modal } from 'react-native';
import { BlurView } from 'expo-blur';
import NameEntry, { checkNameInput } from './Name Entry';

/**
 * This modal opens if the app has not been opened before,
 * it allows the user to chose a name and informs them of the
 * limitations of the language model in use.
 * @param {object} activeTheme an object containing values for the current theme.
 * @param {boolean} state a value for opening or closing the modal.
 * @returns {Modal} modal is triggered to open from App.jsx based on whether the name value is null or not.
 */
export default function StarterPage({ activeTheme, state }) {
    const [name, setName] = useState('');
    const [displayState, setDisplayState] = useState(false);
    const [localState, setLocalState] = useState(state);

    useEffect(() => {
        if (!state) {
            setLocalState(false);
        } else {
            setLocalState(true);
        }
    }, [state]);

    return (
        <Modal
            transparent={true}
            visible={localState}
            animationType='fade'
            style={[styles.modalContainer]}>
            <BlurView
                style={styles.blurView}
                tint='systemThinMaterial'
                intensity={80}>
                <View
                    style={[
                        styles.modalItself,
                        { backgroundColor: activeTheme.modalColour },
                    ]}>
                    {displayState ? (
                        <View>
                            <Text style={{ fontSize: 30, alignSelf: 'center' }}>
                                Hello {name}!
                            </Text>
                            <Text style={styles.smallText}>
                                This service utilises language model technology,
                                this technology has a random nature which could
                                lead to unexpected answers. This language model
                                is designed for weather information primarily
                                but does have some outside conversational
                                ability but for the best results it is advised
                                to focus conversations on weather information.
                            </Text>
                            <Pressable
                                onPress={() => setLocalState(false)}
                                style={styles.submitButton}>
                                <Text>I understand</Text>
                            </Pressable>
                        </View>
                    ) : (
                        <View style={styles.subContainer}>
                            <Text style={styles.titleText}>
                                Before we start...
                            </Text>
                            <Text style={styles.questionText}>
                                Why don't you tell me your name?
                            </Text>

                            <NameEntry
                                name={name}
                                setName={setName}
                            />

                            <Text style={styles.smallText}>
                                Use of your name is purley to provide a more
                                natural dialogue and is not used to identify you
                                in any way.
                            </Text>

                            <Pressable
                                style={styles.submitButton}
                                onPress={() => {
                                    checkNameInput(name);
                                    setDisplayState(true);
                                }}>
                                <Text>Confirm</Text>
                            </Pressable>
                        </View>
                    )}
                </View>
            </BlurView>
        </Modal>
    );
}

const styles = StyleSheet.create({
    modalItself: {
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: '30%',
        width: '80%',
        height: '70%',
        alignSelf: 'center',
        borderRadius: 50,
    },
    submitButton: {
        alignSelf: 'center',
        backgroundColor: 'lightgreen',
        padding: 10,
        borderRadius: 50,
        borderWidth: 3,
        padding: 10,
    },
    modalContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    inputContainer: {
        borderRadius: 50,
        borderWidth: 3,
        flex: 0.1,
        width: '75%',
        height: 10,
    },
    blurView: {
        flex: 1,
    },
    titleText: {
        fontSize: 30,
        textAlign: 'auto',
        position: 'absolute',
        top: 20,
    },
    questionText: {
        margin: 10,
        fontSize: 20,
    },
    smallText: {
        fontSize: 20,
        margin: 10,
    },
    subContainer: {
        flex: 1,
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center',
    },
    confirmButton: {
        alignSelf: 'center',
        backgroundColor: 'lightGreen',
        padding: 10,
    },
});
