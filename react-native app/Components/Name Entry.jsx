/**
 * @file A component and logic pertaining to manipulation of the user's chosen name.
 * @module NameEntry
 */
import { Alert, StyleSheet, TextInput, View } from 'react-native';
import { setUserName } from '../Logic/Manipulation';

/**
 * A TextInput specifically for the user's to enter their chosen name.
 * @param {string} name value representing what the user has entered into the TextInput.
 * @param {function} setName a function to change the value of name.
 * @returns
 */
export default function NameEntry({ name, setName }) {
    return (
        <View style={styles.container}>
            <TextInput
                value={name}
                onChangeText={setName}
            />
        </View>
    );
}

/**
 * A function for sanitising what the user enters into the the name entry.
 * @param {string} name the user's input
 * @returns {boolean} represent whether what the user has entered is acceptable.
 */
export const checkNameInput = (name) => {
    if (name == '') {
        Alert.alert(
            `Please enter a name. It doesn't have to be your real one.`
        );
        return false;
    } else if (name.length >= 32) {
        Alert.alert('Sorry but this is too long.');
        return false;
    } else {
        setUserName(name);
        return true;
    }
};

const styles = StyleSheet.create({
    container: {
        borderWidth: 3,
        borderRadius: 50,
        width: '60%',
        padding: 10,
    },
});
