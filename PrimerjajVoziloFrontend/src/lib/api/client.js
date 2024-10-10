import { error } from '@sveltejs/kit';
import { writable } from 'svelte/store';


const BASE_PATH = "http://localhost:8000//api";


function createVehiclesStore() {
    const { subscribe, set, update } = writable([]);

    return {
        subscribe,
        addVehicle: (vehicle) => update((vehicles) => [...vehicles, vehicle]),
        removeVehicle: (vehicle) => update((vehicles) => {vehicles.splice(vehicles.indexOf(vehicle), 1); return vehicles})
    };
}

export const vehiclesStore = createVehiclesStore();


export async function getVehicle(url) {
    const _url = BASE_PATH + `/get-vehicle?url=${url}`;
    const response = await fetch(_url);

    if (!response.ok) {
        return {
            error: "Problem"
        };
    }

    return {
        vehicle: await response.json()
    };
}


// Login in and return auth token
export async function login(email, password) {
    const url = BASE_PATH + "/auth/get-token/";
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({
            username: email, password
        }),
        headers: myHeaders
    });

    if (!response.ok) {
        return {
            error: "Problem"
        };
    }

    return await response.json();
}


// Lookup user info using token
export async function userLookup(token) {
    const url = BASE_PATH + "/auth/user/";
    const myHeaders = new Headers();
    myHeaders.append("Authorization", `Bearer ${token}`);
    const response = await fetch(url, {
        headers: myHeaders
    });

    if (!response.ok) {
        return {
            error: "Problem"
        };
    }

    return await response.json();
}