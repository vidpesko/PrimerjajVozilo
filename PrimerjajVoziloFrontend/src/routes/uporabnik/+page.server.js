import { userLookup } from "$lib/api/client.js";

export async function load({ cookies }) {
    const token = cookies.get("session_token");
    const user = await userLookup(token);

    return {
        user
    };
}