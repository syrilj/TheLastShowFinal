import { useState } from "react";
import { useParams, useOutletContext } from 'react-router-dom';

function WriteNew(){
    const[obituaries, uuid, setObituaries] = useOutletContext();

    const [name, setName] = useState("");
    const [when, setWhen] = useState("");
    const [death, setDeath] = useState("");
    const [file, setFile] = useState(null);
    console.log("uuid: ", uuid)

    const handleAddObituary = (obituary) => {
        setObituaries([...obituaries, obituary]);
    };
    

    const onSubmitForm = async (e) => {
        e.preventDefault();

    
        const data = new FormData();
        data.append("file", file);
        data.append("name", name);
        data.append("when", when);
        data.append("death", death);
        console.log(data);
        try {
            // Make API call to server to create obituary
            const response = await fetch("https://34seqfyek6m3nilto6ndl2i6li0mhxhl.lambda-url.ca-central-1.on.aws/", {
                method: "POST",
                body: data,
                headers: {
                    "uuid": uuid
                }
            });

    
            if (response.ok) {
                // Obituary created successfully
                const result = await response.json();
                // const { obituary_text, audio_filename } = result;
                // console.log("Obituary created successfully:", obituary_text, audio_filename);
                handleAddObituary(result);
                //add new obituary to the list of obituaries

                // Redirect user to desired page later once other components are implemented
                // window.location.href = "/";
            } else {
                // Handle error response
                console.error("Failed to create obituary:", response.statusText);
            }
        } catch (error) {
            // Handle network or server error
            console.error("Failed to create obituary:", error);
        }
        window.location.href = "/";
    };
    
    const onFileChange = (e) => {
        console.log(e.target.files);
        setFile(e.target.files[0]);
    };

    return (
        <div className="WriteNew">
            <h2 className="WriteNewobituarytext"> Create a New Obituary</h2>
            <form className="formdiv" onSubmit={onSubmitForm}>
                <div className="imgselectdiv">
                    <input
                        className="imgselect"
                        type="file"
                        required
                        accept="images/*"
                        onChange={onFileChange}
                    />
                </div>
               
                <div className="nameboxdiv"> 
                    <input 
                        className="namebox"
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Name of the deceased"
                        required
                    /> 
                </div>

                <i>Born:  </i> 
                <input
                    className="birthselect"
                    value={when}
                    onChange={(e) => setWhen(e.target.value)}
                    type="datetime-local"
                    required
                />

                &emsp; &emsp; &emsp; &emsp; &emsp; 
                <i>Died:  </i> 
                <input
                    className="deathselect"
                    value={death}
                    onChange={(e) => setDeath(e.target.value)}
                    type="datetime-local"
                    required
                />

                <button className="writeobituarybutton"> Write Obituary</button>
            </form>
        </div>
    );
}

export default WriteNew;
