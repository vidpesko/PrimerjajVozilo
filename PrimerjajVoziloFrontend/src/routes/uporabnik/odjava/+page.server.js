import { redirect } from '@sveltejs/kit';

export function load({ cookies }) {
    cookies.delete("logged_in", {path: "/"});
    cookies.delete("session_token", {path: "/"});

    throw redirect(307, "/primerjaj");
}