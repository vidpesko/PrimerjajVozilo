import { getVehicle } from "$lib/api/client.js";
import { fail } from "@sveltejs/kit";


const URL_VALIDATION_PATTERN = "https://www.avto.net/Ads/details.asp"


export function load({ url }) {
    // Get all vehicles in url
    const vehicles = [...url.searchParams.getAll("vozilo"), ];
}

export const actions = {
    dodaj: async ({ cookies, request }) => {
        const data = await request.formData();
        const inputUrl = data.get("url");
        
        // Validation
        let error = null;
        if (!inputUrl) {
            error = "Polje ne sme biti prazno";
        } else if (!inputUrl.includes(URL_VALIDATION_PATTERN)) {
            error = "Povezava ni pravilna";
        }
        if (error) {
            return fail(422, {
                url: inputUrl,
                error
            });
        }
        
        // Call API
        const response = await getVehicle(inputUrl);
        
        // Check if successful
        if (response.error) {
            return fail(422, {
                url: inputUrl,
                error: response.error
            })
        }

        // Return response
        return response.vehicle
    },
    odstrani: async ({ request }) => {
        const data = await request.formData();
        const vehicle = data.get("vehicle");

        
    }
};