global mesh_precision;
global horizontal;
global vertical;
global goal;

mesh_precision = 10;
horizontal = 200;
vertical = 100;
goal = [99,99];

function mesh_coordinates = mesh_coordinates(position)
  global vertical;
  global horizontal;
  global mesh_precision;
  mesh_coordinates = [round(position(1)*mesh_precision/min(horizontal,vertical))+1,round(position(2)*mesh_precision/min(horizontal,vertical))+1];
endfunction

function neighbours = get_neighbours(mesh_coordinate)
  global horizontal;
  global vertical;
  neighbours = [];
  if mesh_coordinate(1)-1>0
    neighbours = [neighbours;[mesh_coordinate(1)-1,mesh_coordinate(2)]];
  endif
  if mesh_coordinate(1)+1<=mesh_coordinates([horizontal,vertical])(1)
    neighbours = [neighbours;[mesh_coordinate(1)+1,mesh_coordinate(2)]];
  endif
  if mesh_coordinate(2)-1>0
    neighbours = [neighbours;[mesh_coordinate(1),mesh_coordinate(2)-1]];
  endif
  if mesh_coordinate(2)+1<=mesh_coordinates([horizontal,vertical])(2)
    neighbours = [neighbours;[mesh_coordinate(1),mesh_coordinate(2)+1]];
  endif
endfunction

function heuristic = get_heuristic(mesh_coordinate)
  global goal;
  heuristic = abs(mesh_coordinate(1)-mesh_coordinates(goal)(1))+abs(mesh_coordinate(2)-mesh_coordinates(goal)(2));
endfunction

function path = astar(position)
  global goal;
  mesh_coordinate = mesh_coordinates(position);
  queue = [mesh_coordinate,get_heuristic(mesh_coordinate),0];
  explored = []
  while not size(queue)==0
    mesh_coordinate = queue(1,:);
    explored = [explored;mesh_coordinate];
    if mesh_coordinate==goal
      return
    queue = queue(2:end,:);
    neighbours = get_neighbours(mesh_coordinate);
    old_index = ismember(mesh_coordinate,queue(:,1:2));
    for i=1:size(neighbours)
      index = ismember(neighbours(i,:),queue(:,1:2));
      if not index and not ismember(neighbours(i,:),explored)
        queue = [queue;[neighbours(i,:),queue(old_index,:)(4)+1+get_heuristic(neighbours(i,:)),queue(old_index,:)(4)+1]];
      elseif queue(index,:)(4)>queue(old_index,:)(4)+1
        queue(index,:) = [neighbours(i,:),queue(old_index,:)(4)+1+get_heuristic(neighbours(i,:)),queue(old_index,:)(4)+1];
    [s,i] = sort(queue(:,3));
    queue=queue(i,:);
  return
endfunction

astar([10,10])