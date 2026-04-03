/**
 * @file a file containing logic for accessing the devices location services
 * @module Location
 */
import {
    requestForegroundPermissionsAsync,
    getCurrentPositionAsync,
} from 'expo-location';
import { setLocation, setLocationAccess } from './Manipulation';

/**
 * An asynchronous function for getting location service permission and the location values.
 * @returns {null} if the location access or data is unable to be gained then null is returned
 * @returns {object} the user's device location data is return in a object
 */
export default async function getLocationAndPerm() {
    let { status } = await requestForegroundPermissionsAsync();
    if (status !== 'granted') {
        console.error('Location permissions were denied');
        setLocationAccess(false);
        return null;
    } else {
        try {
            const currentPosition = await getCurrentPositionAsync({});
            setLocation(currentPosition);
        } catch (error) {
            console.error('Error getting location:', error);
            return null;
        }
    }
}
