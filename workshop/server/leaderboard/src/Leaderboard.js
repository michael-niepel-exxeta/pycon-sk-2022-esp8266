import { useState } from "react";
import { useQuery, useMutation } from "react-query";
import {fetchScores, fetchLastScores, updateScore} from "./api";

function LeaderboardItem({ score }) {
  return (
    <li key={score.id} className="py-4">
      <div className="grid grid-flow-col gap-4">
        <div className="text-left">
          <p className="text-lg font-medium text-gray-900">{score.name}</p>
        </div>
        <div className="text-right">
          <p className="text-lg text-gray-500">{score.time}</p>
        </div>
      </div>
    </li>
  );
}

function Table() {
  const { isLoading, data } = useQuery("scores", fetchScores, { refetchInterval: 2000 });
  return (
    !isLoading && (
      <ul className="divide-y divide-gray-200">
        {data.map((score) => (
          <LeaderboardItem key={score.id} score={score} />
        ))}
      </ul>
    )
  );
}

const LastScoreForm = ({ data }) => {
  const [name, setName] = useState("");
  const mutation = useMutation(updateScore);

  const onSubmit = (event) => {
    console.log("submit", event);
    event.preventDefault();
    mutation.mutate({
      id: data.id,
      name: name,
    });
  };

  return (
    <form className="m-4" onSubmit={onSubmit}>
      <div>
        <input placeholder="Enter name..." className="rounded" type="text" value={name} onChange={(e) => setName(e.target.value)} />
        {data.time}
      </div>
    </form>
  );
};

function Leaderboard() {
  const { isLoading, data } = useQuery("fetchLastScore", fetchLastScores, { refetchInterval: 1000 });

  return !isLoading && data.length > 0 && (data[0].name == null ? <LastScoreForm data={data[0]} /> : <Table />);
}

export default Leaderboard;
