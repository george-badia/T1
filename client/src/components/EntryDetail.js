// import React from "react";
// import { Link } from "react-router-dom";

// function EntryDetail({ entry }) {
//   return (
//     <div className="card">
//       <div className="card-body">
//         <h5 className="card-title">{entry.location}</h5>
//         <h6 className="card-subtitle mb-2 text-muted">
//           {new Date(entry.date).toLocaleDateString()}
//         </h6>
//         <p className="card-text">{entry.description}</p>
//         <Link to={`/entries/edit/${entry.id}`} className="btn btn-primary me-2">
//           Edit
//         </Link>
//         <Link to="/" className="btn btn-secondary">
//           Back to Home
//         </Link>
//       </div>
//     </div>
//   );
// }

// export default EntryDetail;
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getEntry } from "../utils/api";
import TagList from "./TagList";
import TagInput from "./TagInput";

function EntryDetail({ entryId }) {
  const [entry, setEntry] = useState(null);

  useEffect(() => {
    const fetchEntry = async () => {
      try {
        const response = await getEntry(entryId);
        setEntry(response.data);
      } catch (error) {
        console.error("Error fetching entry:", error);
      }
    };
    fetchEntry();
  }, [entryId]);

  const handleTagAdded = (newTag) => {
    setEntry((prevEntry) => ({
      ...prevEntry,
      tags: [...prevEntry.tags, newTag],
    }));
  };

  if (!entry) return <div className="text-center">Loading...</div>;

  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">{entry.location}</h5>
        <h6 className="card-subtitle mb-2 text-muted">
          {new Date(entry.date).toLocaleDateString()}
        </h6>
        <p className="card-text">{entry.description}</p>
        <div className="mb-3">
          <h6>Tags:</h6>
          <TagList tags={entry.tags} />
          <TagInput entryId={entry.id} onTagAdded={handleTagAdded} />
        </div>
        <Link to={`/entries/edit/${entry.id}`} className="btn btn-primary me-2">
          Edit
        </Link>
        <Link to="/" className="btn btn-secondary">
          Back to Home
        </Link>
      </div>
    </div>
  );
}

export default EntryDetail;
