/**
 * @file The primary file used as the front page of the application. First code to run.
 * @module App
 */
import { Feather } from '@expo/vector-icons';
import { useEffect, useState } from 'react';
import {
    Alert,
    KeyboardAvoidingView,
    Platform,
    Pressable,
    StyleSheet,
    TextInput,
    View,
} from 'react-native';
import { getTheme, getUserName, setTheme } from './Logic/Manipulation';
import { impactAsync } from 'expo-haptics';

import MessageDisplay from './Components/Message Display';
import Settings from './Components/Settings';
import StarterPage from './Components/Starter Page';

/**
 * The core component housing all others.
 * @returns {View} The primary view component where all other components reside underneath.
 */
export default function App() {
    const colourJson = require('./assets/json/theme.json');

    const [userInput, setInput] = useState('');
    const [send, setSend] = useState(false);
    const [themeSate, setThemeState] = useState(true);
    const [activeTheme, setActiveTheme] = useState(colourJson.darkColours);
    const [askName, setAskName] = useState(false);
    const [locationAccess, setAccess] = useState(false);

    useEffect(() => {
        const fetchTheme = async () => {
            const fetchedTheme = await getTheme();
            setThemeState(fetchedTheme);
        };
        const fetchName = async () => {
            const fetchedName = await getUserName();
            if (fetchedName == null) {
                setAskName(true);
            }
        };

        fetchTheme();
        fetchName();
    }, []);

    useEffect(() => {
        if (themeSate) {
            setActiveTheme(colourJson.darkColours);
        } else {
            setActiveTheme(colourJson.lightColours);
        }
    }, [themeSate]);

    /**
     * Sanitises the user's message
     */
    const handleMessageSend = () => {
        impactAsync();
        if (userInput.trim() == '') {
            Alert.alert('Message is blank.');
        } else if (userInput.length >= 256) {
            Alert.alert('Message is too long.');
        } else {
            setSend(true);
        }
    };

    if (Platform.OS === 'ios') {
        () => setInputSize({ height: 100 });
    }

    return (
        <View
            style={[
                styles.container,
                { backgroundColor: activeTheme.primary },
            ]}>
            <StarterPage
                activeTheme={activeTheme}
                state={askName}
                setState={setAskName}
            />
            <MessageDisplay
                send={send}
                setSend={setSend}
                userMessage={userInput}
                setUserInput={setInput}
            />
            <View style={styles.topArea}>
                <Settings
                    activeTheme={activeTheme}
                    setAccess={setAccess}
                    locationAccess={locationAccess}
                />
                <Pressable
                    onPress={() => {
                        impactAsync();
                        const newState = !themeSate;
                        setThemeState(newState);
                        setTheme(newState);
                    }}
                    style={[
                        styles.themeButton,
                        { backgroundColor: activeTheme.secondary },
                    ]}>
                    {themeSate ? (
                        <View>
                            <Feather
                                name='sun'
                                color={activeTheme.primary}
                                size={50}
                            />
                        </View>
                    ) : (
                        <View>
                            <Feather
                                name='moon'
                                color={activeTheme.primary}
                                size={50}
                            />
                        </View>
                    )}
                </Pressable>
            </View>
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
                <View
                    style={[
                        styles.inputArea,
                        {
                            borderColor: activeTheme.secondary,
                            backgroundColor: activeTheme.primary,
                        },
                    ]}>
                    <TextInput
                        style={[
                            styles.input,
                            {
                                color: activeTheme.secondary,
                            },
                        ]}
                        value={userInput}
                        onChangeText={setInput}
                    />
                    <Pressable
                        style={[
                            styles.sendButton,
                            { backgroundColor: activeTheme.secondary },
                        ]}
                        onPress={() => handleMessageSend()}>
                        <Feather
                            name='send'
                            size={35}
                            color={activeTheme.primary}
                        />
                    </Pressable>
                </View>
            </KeyboardAvoidingView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        width: '100%',
        height: '100%',
        alignItems: 'center',
        justifyContent: 'center',
    },
    themeButton: {
        position: 'absolute',
        top: 10,
        right: 10,
        padding: 5,
        borderRadius: 50,
        margin: 20,
    },
    inputArea: {
        bottom: 20,
        marginTop: 1,
        flexDirection: 'row',
        borderWidth: 3,
        borderRadius: 50,
        padding: 10,
        width: '80%',
    },
    sendButton: {
        borderRadius: 50,
        width: 45,
        height: 45,
        alignContent: 'center',
        justifyContent: 'center',
    },
    topArea: {
        flex: 0.1,
        marginTop: 10,
        width: '100%',
        position: 'absolute',
        top: 20,
        flexDirection: 'row',
    },
    input: {
        width: '75%',
        flex: 1,
        alignContent: 'center',
        alignSelf: 'center',
        height: '100%',
    },
});
