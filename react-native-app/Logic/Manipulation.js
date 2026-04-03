/**
 * @file Contains all logic pertaining to storage manipulation
 * @module Manipulation
 */
import AsyncStorage from '@react-native-async-storage/async-storage';

/**
 * Wraps a object in a string for storage purposes
 * @param {object} json
 * @returns {string} json wrapped in a string
 */
function jsonParseIn(json) {
    const jsonAsString = JSON.stringify(json);
    return jsonAsString;
}

/**
 * Parses a string into an object
 * @param {string} string
 * @returns {object} the string parsed an object so the values may be used
 */
function jsonParseOut(string) {
    const json = string ? JSON.parse(string) : null;
    return json;
}

/**
 * Sets the value of the theme in storage so the user's choice is remembered
 * @param {boolean} theme a boolean value representing dark or light theme
 */
export async function setTheme(theme) {
    try {
        await AsyncStorage.setItem('theme', jsonParseIn(theme));
    } catch (e) {
        console.error('err in setTheme ', e);
    }
}

/**
 * Fetches the stored value representing the user's chosen theme
 * @returns {boolean} a boolean value representing dark or light theme
 */
export async function getTheme() {
    try {
        const themeAsString = await AsyncStorage.getItem('theme');
        return jsonParseOut(themeAsString);
    } catch (e) {
        console.error('err in getTheme ', e);
    }
}

/**
 * A function for storing the user's chosen name
 * @param {string} name the user's chosen name
 */
export async function setUserName(name) {
    try {
        await AsyncStorage.setItem('name', name);
    } catch (e) {
        console.error('err in setUserName ', e);
    }
}
/**
 * A function for fetching the user's chosen name from storage
 * @returns {string} the stored name
 */
export async function getUserName() {
    try {
        const name = await AsyncStorage.getItem('name');
        return name;
    } catch (e) {
        console.error('err in getUserName', e);
    }
}

// remove before submitting
export async function resetName() {
    try {
        await AsyncStorage.removeItem('name');
    } catch (e) {
        console.error('err in resetName ', e);
    }
}

/**
 * A function for storing whether the device's location are accessible
 * @param {boolean} value a value representing with access has been granted
 */
export async function setLocationAccess(value) {
    try {
        await AsyncStorage.setItem('locationAccess', jsonParseIn(value));
    } catch (e) {
        console.error('err in setLocationAccess ', e);
    }
}

/**
 * A function for fetching the value representing whether device location access has been granted.
 * @returns {object} the value representing location access
 */
export async function getLocationAccess() {
    try {
        const locationAccess = await AsyncStorage.getItem('locationAccess');
        return jsonParseOut(locationAccess);
    } catch (e) {
        console.error('err in getLocationAccess ', e);
    }
}

/**
 * A function for getting the storage value of the user's location
 * @returns  {string} a object wrapped in a string containing the value for the user's location
 */
export async function getLocation() {
    try {
        const location = await AsyncStorage.getItem('location');
        return location;
    } catch (e) {
        console.error('err in getLocation ', e);
    }
}

/**
 * A function for storing the user's location values
 * @param {object} value an object containing data relating to the user's location
 */
export async function setLocation(value) {
    try {
        await AsyncStorage.setItem('location', jsonParseIn(value));
    } catch (e) {
        console.error('err in setLocation ', e);
    }
}
