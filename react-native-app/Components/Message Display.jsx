/**
 * @file Contains all react-native components focused on displaying the user and LM's messages.
 * @module MessageDisplay
 */
import { useEffect, useState } from 'react';
import {
    KeyboardAvoidingView,
    Platform,
    ScrollView,
    StyleSheet,
    Text,
    View,
} from 'react-native';
import { sendMessage } from '../Logic/Api';
import Markdown from 'react-native-markdown-display';
import { impactAsync } from 'expo-haptics';
/**
 * A react native component for displaying messages.
 * @param {boolean} send a boolean value denoting whether to send the user's message or not.
 * @param {function} setSend changes the value of send.
 * @param {string} userMessage the user's message to be sent.
 * @param {function} setUserInput changes the value in the text entry box.
 * @returns {View} A view where the messages will be displayed.
 */
export default function MessageDisplay({
    send,
    setSend,
    userMessage,
    setUserInput,
}) {
    const [displayStack, setDisplayStack] = useState([]);

    useEffect(() => {
        /**
         * A simple function for asynchronously fetching the message from the speaker
         * and updating relevant stacks for display purposes.
         */
        const fetchSpeakerMessage = async () => {
            const fetchedMsg = await sendMessage(userMessage);
            if (typeof fetchedMsg === 'string') {
                updateDisplayStack(
                    messageBubble({ message: fetchedMsg, source: 'error' })
                );
            } else {
                const message = fetchedMsg[0].response;
                updateDisplayStack(
                    messageBubble({
                        message: message,
                        source: 'speaker',
                    })
                );
            }
        };

        if (send && userMessage.trim() !== '') {
            updateDisplayStack(
                messageBubble({ message: userMessage, source: 'user' })
            );
            fetchSpeakerMessage();
            setSend(false);
            setUserInput('');
        }
    }, [send, userMessage, setSend, setUserInput]);

    /**
     * Appends a message component onto display stack.
     * @param {View} item the message component to be added to stack.
     */
    const updateDisplayStack = (item) => {
        setDisplayStack((prevStack) => [...prevStack, item]);
    };

    /**
     * A component for displaying a message from either the user, speaker (LM) or an error.
     * @param {string} message the message from either the user or speaker (LM)
     * @returns {View} the message wrapped in a view component to be displayed.
     */
    const messageBubble = (message) => {
        const source = message.source;
        const text = message.message;
        console.log(text);
        let colour = '#F3470C';
        let messageText = null;

        if (source == 'user') {
            colour = '#0CB8F3';
            messageText = <Text style={styles.messageText}>{text}</Text>;
        }
        if (source == 'speaker') {
            impactAsync();
            messageText = (
                <View style={{ padding: 10 }}>
                    <Markdown style={{ body: styles.messageText }}>
                        {text}
                    </Markdown>
                </View>
            );
        } else {
            messageText = <Text style={styles.messageText}>{text}</Text>;
        }

        return (
            <View
                style={[styles.messageContainer, { backgroundColor: colour }]}>
                {messageText}
            </View>
        );
    };
    return (
        <View style={styles.container}>
            <KeyboardAvoidingView
                behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
                <View style={{ flex: 1, margin: 1 }}>
                    <ScrollView
                        style={styles.scrollView}
                        ref={(ref) => {
                            // fragment from https://stackoverflow.com/a/42736127
                            this.scrollView = ref;
                        }}
                        onContentSizeChange={() => {
                            this.scrollView.scrollToEnd({ animated: true });
                        }}>
                        <View style={{ flex: 1 }}>
                            {displayStack.map((message, index) => (
                                <View key={index}>{message}</View>
                            ))}
                        </View>
                    </ScrollView>
                </View>
            </KeyboardAvoidingView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 2,
    },
    messageContainer: {
        borderRadius: 50,
        padding: 10,
        alignSelf: 'center',
        maxWidth: '80%',
        margin: 10,
    },
    scrollView: {
        marginTop: '25%',
        width: '100%',
        marginBottom: 2,
    },
    innerView: {
        width: '100%',
        alignItems: 'center',
    },
    messageText: {
        textAlign: 'center',
        fontSize: 20,
    },
});
