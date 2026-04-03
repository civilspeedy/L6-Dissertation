/**
 * @file Contains logic pertaining to http api requests with the webserver
 * @module Api
 */
import { getLocation, getUserName } from './Manipulation';
import axios from 'axios';

/**
 * Used for context.
 */
let isNewChat = true;

/**
 * An asynchronous function that sends a http request to the webserver on local-host and returns the response.
 * @param {string} message the user's message
 * @returns {string} the response from the webserver or an error message should a failure occur.
 */
export const sendMessage = async (message) => {
    const name = await getUserName();
    let location = await getLocation();
    if (location == null) {
        location = 'None';
    }
    const request = `http://192.168.4.120:5000/communicate?message=${message}&name=${name}&location=${location}&chatStatus=${isNewChat}`;
    try {
        const response = await axios.get(request);
        isNewChat = false;
        if (response.data[0].response === null) {
            return "Couldn't process that, please try a different input.";
        } else {
            return response.data;
        }
    } catch (e) {
        console.log(e);
        return 'Something has gone wrong, please try again.';
    }
};
