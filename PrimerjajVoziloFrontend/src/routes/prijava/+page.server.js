import { redirect } from '@sveltejs/kit';
import { fail } from "@sveltejs/kit";
import { login } from "$lib/api/client.js";

export const actions = {
    prijavi: async ({cookies, request}) => {
        const data = await request.formData();
        const email = data.get("email");
        const password = data.get("password");

        const response = await login(email, password);

        if (response.token) {
            cookies.set("session_token", response.token, { path: "/"});
            cookies.set("logged_in", "true", { path: "/"});
            throw redirect(307, "/");
        } else {
            return fail(401, {error: response})
        }
    }
}