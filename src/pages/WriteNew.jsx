import { useState } from "react";
import { useOutletContext } from 'react-router-dom';

function WriteNew(){
    const[obituaries, uuid, setObituaries] = useOutletContext();

    const [name, setName] = useState("");
    const [when, setWhen] = useState("");
    const [death, setDeath] = useState("");
    const [file, setFile] = useState(null);

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

        try{
            const res = await fetch("https://34seqfyek6m3nilto6ndl2i6li0mhxhl.lambda-url.ca-central-1.on.aws/", {
                method: "POST",
                body: data,
                headers: {
                    'uuid': uuid
                }
            });
            const body = await res.json();
            handleAddObituary(body);
            window.location = "/";
        }
        catch(err){
            console.error(err.message);
        }
    };
    
    const onFileChange = (e) => {
        console.log(e.target.files);
        setFile(e.target.files[0]);
    };

    return (
        <div className="flex flex-col gap-10 mt-20 items-center h-full">
            <h2 className="text-3xl font-bold "> Create a New Obituary</h2>
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
