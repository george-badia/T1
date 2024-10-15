// import React, { useState } from "react";
// import { uploadPhoto } from "../utils/api";

// function PhotoUpload({ entryId, onPhotoUploaded }) {
//   const [file, setFile] = useState(null);

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (file) {
//       const formData = new FormData();
//       formData.append("photo", file);
//       try {
//         const response = await uploadPhoto(entryId, formData);
//         onPhotoUploaded(response.data);
//         setFile(null);
//       } catch (error) {
//         console.error("Error uploading photo:", error);
//       }
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <div className="mb-3">
//         <input
//           type="file"
//           onChange={handleFileChange}
//           className="form-control"
//         />
//       </div>
//       <button type="submit" className="btn btn-primary" disabled={!file}>
//         Upload Photo
//       </button>
//     </form>
//   );
// }

// export default PhotoUpload;
// // import React, { useState } from "react";
// // import { uploadPhoto } from "../utils/api";

// // function PhotoUpload({ entryId, onPhotoUploaded }) {
// //   const [photoUrl, setPhotoUrl] = useState("");

// //   const handleUrlChange = (e) => {
// //     setPhotoUrl(e.target.value);
// //   };

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     if (photoUrl) {
// //       try {
// //         // Assuming your API accepts a JSON payload with a photo URL
// //         const response = await uploadPhoto(entryId, { photoUrl });
// //         onPhotoUploaded(response.data);
// //         setPhotoUrl("");
// //       } catch (error) {
// //         console.error("Error uploading photo URL:", error);
// //       }
// //     }
// //   };

// //   return (
// //     <form onSubmit={handleSubmit}>
// //       <div className="mb-3">
// //         <input
// //           type="text"
// //           value={photoUrl}
// //           onChange={handleUrlChange}
// //           placeholder="Enter photo URL"
// //           className="form-control"
// //         />
// //       </div>
// //       <button type="submit" className="btn btn-primary" disabled={!photoUrl}>
// //         Upload Photo URL
// //       </button>
// //     </form>
// //   );
// // }

// // export default PhotoUpload;
import React, { useState } from "react";
import { uploadPhoto } from "../utils/api";

function PhotoUpload({ entryId, onPhotoUploaded }) {
  const [url, setUrl] = useState("");

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (url) {
      try {
        const response = await uploadPhoto(entryId, { url });
        onPhotoUploaded(response.data);
        setUrl("");
      } catch (error) {
        console.error("Error uploading photo:", error);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="photoUrl" className="form-label">
          Photo URL
        </label>
        <input
          type="url"
          id="photoUrl"
          className="form-control"
          value={url}
          onChange={handleUrlChange}
          placeholder="Enter the URL of the photo"
          required
        />
      </div>
      <button type="submit" className="btn btn-primary" disabled={!url}>
        Add Photo
      </button>
    </form>
  );
}

export default PhotoUpload;
